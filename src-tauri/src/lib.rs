mod command_detect_devices;

use tauri::Manager;
use tauri_plugin_decorum::WebviewWindowExt; // adds helper methods to WebviewWindow


// #[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_http::init())
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_decorum::init())
        .setup(|app| {
            // Create a custom titlebar for main window
            // On Windows this will hide decoration and render custom window controls
            // On macOS it expects a hiddenTitle: true and titleBarStyle: overlay
            let main_window = app.get_webview_window("main").unwrap();
            main_window.create_overlay_titlebar().unwrap();

            #[cfg(target_os = "macos")]
            main_window.set_traffic_lights_inset(16.0, 20.0).unwrap();
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![command_detect_devices::fetch_devices])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
