import { ref } from "vue";
import { defineStore } from "pinia";
import { DeviceInfo, Device } from "@/types/device";
import { invoke } from "@tauri-apps/api/core";
import {
  BaseDirectory,
  create,
  exists,
  mkdir,
  readTextFile,
  writeTextFile,
} from "@tauri-apps/plugin-fs";
import ky from "ky";

export const useDeviceStore = defineStore("devices", () => {
  const devices = ref<Map<string, DeviceInfo>>(new Map());
  const loading = ref(false);
  const detectedDevices = ref(0);

  const initlize = async () => {
    const ifDirectoriesExist = await exists("", {
      baseDir: BaseDirectory.AppData,
    });

    if (!ifDirectoriesExist) {
      await mkdir("", {
        baseDir: BaseDirectory.AppData,
      });
    }

    const ifFileExists = await exists("devices.json", {
      baseDir: BaseDirectory.AppData,
    });

    if (!ifFileExists) {
      await create(`devices.json`, {
        baseDir: BaseDirectory.AppData,
      });

      await writeTextFile("devices.json", JSON.stringify([]), {
        baseDir: BaseDirectory.AppData,
      });
      return;
    }

    try {
      const devicesRaw = await readTextFile("devices.json", {
        baseDir: BaseDirectory.AppData,
      });
      const devicesJson = JSON.parse(devicesRaw || "[]");

      devicesJson.forEach((deviceInfo: DeviceInfo) => {
        if (deviceInfo.address && deviceInfo.device) {
          devices.value.set(deviceInfo.address, deviceInfo);
        }
      });

      await Promise.all(
        Array.from(devices.value.keys()).map((address) =>
          reconnectDevice(address)
        )
      );

      await saveDevicesToFile();
    } catch (err) {
      console.error("Error reading devices.json:", err);
      await writeTextFile("devices.json", JSON.stringify([]), {
        baseDir: BaseDirectory.AppData,
      });
    }
  };

  const reconnectDevice = async (address: string) => {
    const deviceInfo = devices.value.get(address);
    if (!deviceInfo) return;

    try {
      const currentDevice = await fetchDevice(address);
      if (currentDevice) {
        devices.value.set(address, {
          ...currentDevice,
          status: "online",
        });
      } else {
        devices.value.set(address, {
          ...deviceInfo,
          status: "offline",
        });
      }
    } catch (err) {
      devices.value.set(address, {
        ...deviceInfo,
        status: "offline",
      });
    }
  };

  const saveDevicesToFile = async () => {
    try {
      const devicesArray = Array.from(devices.value.values());
      await writeTextFile(
        "devices.json",
        JSON.stringify(devicesArray, null, 2),
        {
          baseDir: BaseDirectory.AppData,
        }
      );
    } catch (err) {
      console.error("Error saving devices to file:", err);
    }
  };

  const addDevice = async (address: string) => {
    loading.value = true;
    const device = await fetchDevice(address);
    if (device) {
      devices.value.set(address, device);
    }
    loading.value = false;
  };

  const fetchDevice = async (address: string): Promise<DeviceInfo | null> => {
    try {
      const device = await ky
        .get(`http://${address}:9012/api/device`, {
          timeout: 1000,
        })
        .json<Device>();
      const deviceInfo: DeviceInfo = {
        status: "online",
        address: address,
        device: device,
      };
      return deviceInfo;
    } catch (err) {
      return null;
    }
  };

  const fetchDevices = async (addresses: string[]) => {
    loading.value = true;
    detectedDevices.value = 0;
    try {
      await Promise.all(
        addresses.map(async (address) => {
          const device = await fetchDevice(address);
          if (device) {
            detectedDevices.value++;
            devices.value.set(address, device);
            return { address, device };
          }
          return null;
        })
      );
      await saveDevicesToFile();
    } catch (err) {
      console.log("Error fetching devices:", err);
    } finally {
      loading.value = false;
    }
  };

  const detectDevices = async (addresses: string[]) => {
    loading.value = true;
    try {
      const results = await invoke<string[]>("fetch_devices", {
        addresses,
      });

      console.log("Detected devices:", results);

      await fetchDevices(results);
    } catch (err) {
    } finally {
      loading.value = false;
    }
  };

  const getDevice = (address: string) => {
    return devices.value.get(address);
  };

  const numberOfDetectedDevices = () => {
    return detectedDevices.value;
  };

  initlize();

  return {
    devices,
    addDevice,
    fetchDevices: detectDevices,
    loading,
    numberOfDetectedDevices,
    getDevice,
  };
});
