package io.github.jackofnonetrades.multi3ify;

import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.channels.FileChannel;
import java.nio.channels.FileLock;
import java.nio.file.AtomicMoveNotSupportedException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;
import java.util.jar.JarFile;
import java.util.jar.Manifest;

/** Installs the metadata-selected mod before RFB/Forge discovers mods. */
public final class Bootstrap {
    static final String MANAGED = "lwjgl3ify-multi3ify-managed.jar";

    private Bootstrap() {}

    public static void main(String[] args) throws Throwable {
        checkRuntime();
        String digest = required("multi3ify.modSha256");
        if (!digest.matches("[a-f0-9]{64}")) {
            throw new IOException("Invalid lwjgl3ify SHA-256 in launcher metadata");
        }
        Path game = Paths.get(".").toAbsolutePath().normalize();
        for (int i = 0; i < args.length - 1; i++) {
            if (args[i].equals("--gameDir")) {
                game = Paths.get(args[i + 1]).toAbsolutePath().normalize();
            }
        }
        Files.createDirectories(game);
        try (FileChannel channel = FileChannel.open(game.resolve(".multi3ify.lock"),
                StandardOpenOption.CREATE, StandardOpenOption.WRITE);
             FileLock lock = channel.tryLock()) {
            if (lock == null) {
                throw new IOException("Another multi3ify launch is updating this instance");
            }
            Path mods = game.resolve("mods");
            Files.createDirectories(mods);
            Path managed = mods.resolve(MANAGED);
            Path download = null;
            try {
                Path source = managed;
                if (!Files.isRegularFile(managed) || !sha256(managed).equals(digest)) {
                    download = Files.createTempFile(mods, ".multi3ify-", ".tmp");
                    System.out.println("[multi3ify] Installing the selected lwjgl3ify version...");
                    download(required("multi3ify.modUrl"), download);
                    source = download;
                }
                install(game, source, digest);
            } finally {
                if (download != null) Files.deleteIfExists(download);
            }
        }
        // Calling on this thread preserves upstream's macOS first-thread entry point.
        String delegate = required("multi3ify.delegate");
        if (!delegate.startsWith("com.gtnewhorizons.retrofuturabootstrap.")) {
            throw new IOException("Unexpected lwjgl3ify launch entry point: " + delegate);
        }
        try {
            Class.forName(delegate).getMethod("main", String[].class).invoke(null, (Object) args);
        } catch (InvocationTargetException e) {
            throw e.getCause();
        }
    }

    private static void checkRuntime() throws IOException {
        // Look for an LWJGL 2-only resource without loading/initializing any LWJGL
        // classes. Loading PointerBuffer here can bind the wrong implementation,
        // and native initialization must remain on upstream's macOS main thread.
        URL legacy = Bootstrap.class.getClassLoader().getResource("org/lwjgl/LWJGLException.class");
        if (legacy != null) {
            throw new IOException("LWJGL 2 is still on this instance's classpath, alongside lwjgl3ify's LWJGL 3.\n"
                    + "In your launcher, select Edit Instance -> Version -> Minecraft -> Change version"
                    + " -> 1.7.10-lwjgl3ify.\n"
                    + "Changing only the Forge version leaves the ordinary Minecraft runtime installed.\n"
                    + "If the special Minecraft profile is already selected, remove the leftover LWJGL 2"
                    + " component or local patch from the Version tab.\n"
                    + "No mods were changed by this launch. Conflicting LWJGL 2 resource: " + legacy);
        }
    }

    private static String required(String name) throws IOException {
        String value = System.getProperty(name);
        if (value == null || value.isEmpty()) throw new IOException("Missing metadata property: " + name);
        return value;
    }

    private static void download(String address, Path destination) throws IOException {
        URL url = new URL(address);
        for (int redirect = 0; redirect < 6; redirect++) {
            if (!url.getProtocol().equals("https")) throw new IOException("Mod downloads require HTTPS");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(20000);
            connection.setReadTimeout(90000);
            connection.setInstanceFollowRedirects(false);
            connection.setRequestProperty("User-Agent", "multi3ify-bootstrap");
            try {
                int status = connection.getResponseCode();
                if (status >= 300 && status < 400) {
                    String location = connection.getHeaderField("Location");
                    if (location == null) throw new IOException("Missing download redirect location");
                    url = new URL(url, location);
                    continue;
                }
                if (status != 200) throw new IOException("lwjgl3ify download returned HTTP " + status);
                try (InputStream input = connection.getInputStream()) {
                    Files.copy(input, destination, StandardCopyOption.REPLACE_EXISTING);
                }
                return;
            } finally {
                connection.disconnect();
            }
        }
        throw new IOException("Too many lwjgl3ify download redirects");
    }

    static String sha256(Path path) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        try (InputStream input = Files.newInputStream(path)) {
            byte[] buffer = new byte[65536];
            int count;
            while ((count = input.read(buffer)) != -1) digest.update(buffer, 0, count);
        }
        StringBuilder hex = new StringBuilder();
        for (byte b : digest.digest()) hex.append(String.format("%02x", b & 255));
        return hex.toString();
    }

    static boolean isLwjgl3ify(Path path) {
        if (!Files.isRegularFile(path) || !path.getFileName().toString().endsWith(".jar")) return false;
        return hasLwjgl3ifyManifest(path);
    }

    private static boolean hasLwjgl3ifyManifest(Path path) {
        try (JarFile jar = new JarFile(path.toFile())) {
            Manifest manifest = jar.getManifest();
            if (manifest == null) return false;
            String plugin = manifest.getMainAttributes().getValue("FMLCorePlugin");
            return "me.eigenraven.lwjgl3ify.core.Lwjgl3ifyCoremod".equals(plugin);
        } catch (IOException e) {
            return false;
        }
    }

    static void install(Path game, Path source, String expectedDigest) throws Exception {
        // Verify before touching either the managed mod or any existing manual copies.
        if (!sha256(source).equals(expectedDigest) || !hasLwjgl3ifyManifest(source)) {
            throw new IOException("lwjgl3ify download failed verification; existing mods were preserved");
        }
        Path mods = game.resolve("mods");
        Files.createDirectories(mods);
        Path managed = mods.resolve(MANAGED);
        List<Path> duplicates = new ArrayList<>();
        for (Path directory : new Path[] {mods, mods.resolve("1.7.10")}) {
            if (!Files.isDirectory(directory)) continue;
            try (DirectoryStream<Path> files = Files.newDirectoryStream(directory, "*.jar")) {
                for (Path file : files) {
                    if (!file.equals(managed) && isLwjgl3ify(file)) duplicates.add(file);
                }
            }
        }
        if (!source.equals(managed)) {
            // Keep a rollback copy of the previous managed version too.
            if (Files.exists(managed)) backup(game, managed);
            try {
                Files.move(source, managed, StandardCopyOption.ATOMIC_MOVE, StandardCopyOption.REPLACE_EXISTING);
            } catch (AtomicMoveNotSupportedException e) {
                Files.move(source, managed, StandardCopyOption.REPLACE_EXISTING);
            }
        }
        for (Path duplicate : duplicates) {
            backup(game, duplicate);
            Files.delete(duplicate);
        }
    }

    private static void backup(Path game, Path file) throws Exception {
        Path backups = game.resolve(".multi3ify-backups");
        Files.createDirectories(backups);
        Path target = backups.resolve(sha256(file) + "-" + file.getFileName());
        if (!Files.exists(target)) Files.copy(file, target);
        System.out.println("[multi3ify] Saved previous mod to " + target);
    }
}
