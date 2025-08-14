import { ref } from "vue";
import { defineStore } from "pinia";
import { DeviceInfo, Device } from "@/types/device";
import ky from "ky";

export const useDeviceStore = defineStore("devices", () => {
  const devices = ref<Map<string, DeviceInfo>>(new Map());
  const loading = ref(false);
  const detectedDevices = ref(0);

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
      const results = await Promise.all(
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
      results.forEach((result) => {
        if (result) {
          devices.value.set(result.address, result.device);
        }
      });
      console.log("Devices:", devices.value);
    } catch (err) {
      console.log("Error fetching devices:", err);
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

  return {
    devices,
    addDevice,
    fetchDevices,
    loading,
    numberOfDetectedDevices,
    getDevice,
  };
});
