import { ref, type Ref } from "vue";
import { defineStore } from "pinia";
import ky from "ky";

interface boradcastChannel {
  bordercast_endpoints: string[];
}

interface Channel {
  name: string;
  trialData: any[];
  eventSource?: EventSource;
}

interface Device {
  address: string;
  name?: string;
  channels: Record<string, Channel>;
}

export const useTrialDataStore = defineStore("trialData", () => {
  const devices: Ref<Record<string, Device>> = ref({});
  const error: Ref<string | null> = ref(null);
  const isLoading = ref(false);
  const DEFAULT_TIMEOUT = 5000;

  const fetchChannels = async (device_address: string) => {
    const url = `http://${device_address}:9012/api/broadcast/data`;
    try {
      const channels = await ky
        .get(url, { timeout: 1000 })
        .json<boradcastChannel>();
      channels.bordercast_endpoints.forEach((channel_name) => {
        devices.value[device_address].channels[channel_name] = {
          name: channel_name,
          trialData: [],
        };
      });
    } catch (err) {
      console.error("fetchChannels error:", err);
    }
  };

  const connectSSE = async (
    device_address: string,
    channel_name: string,
    callback?: (data: any) => void,
    timeout: number = DEFAULT_TIMEOUT,
  ): Promise<EventSource> => {
    return new Promise((resolve, reject) => {
      isLoading.value = true;
      error.value = null;

      if (!devices.value[device_address]) {
        devices.value[device_address] = {
          address: device_address,
          channels: {},
        };
      }

      const device = devices.value[device_address];
      if (!device.channels[channel_name]) {
        device.channels[channel_name] = {
          name: channel_name,
          trialData: [],
        };
      }

      const channel = device.channels[channel_name];

      channel.eventSource?.close();

      const timeoutId = setTimeout(() => {
        channel.eventSource?.close();
        error.value = `connect timeout (${timeout}ms)`;
        isLoading.value = false;
        reject(new Error(`Connection timeout after ${timeout}ms`));
      }, timeout);

      try {
        const url = `http://${device_address}:9012/api/broadcast/data/${channel_name}`;
        console.log("connectSSE:", url);
        const eventSource = new EventSource(url);
        channel.eventSource = eventSource;

        const onOpen = () => {
          clearTimeout(timeoutId);
          isLoading.value = false;

          eventSource.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              channel.trialData.push(data);
              callback?.(data);
            } catch (err) {
              console.error("SSE data parsing error:", err);
              error.value = `data parsing error: ${channel_name}`;
            }
          };

          resolve(eventSource);
        };

        const onError = () => {
          clearTimeout(timeoutId);
          eventSource.close();
          error.value = `connect failed: ${channel_name}`;
          isLoading.value = false;
          reject(new Error(`SSE connection error`));
        };

        eventSource.addEventListener("open", onOpen, { once: true });
        eventSource.addEventListener("error", onError, { once: true });
      } catch (err) {
        clearTimeout(timeoutId);
        error.value = `failed to create connection: ${
          err instanceof Error ? err.message : String(err)
        }`;
        isLoading.value = false;
        reject(err);
      }
    });
  };

  const disconnectSSE = (device_address: string, channel_name: string) => {
    const channel = devices.value[device_address]?.channels[channel_name];
    channel?.eventSource?.close();
    channel && (channel.eventSource = undefined);
  };

  const getChannelData = (device_address: string, channel_name: string) => {
    return (
      devices.value[device_address]?.channels[channel_name]?.trialData || []
    );
  };

  return {
    devices,
    error,
    isLoading,
    connectSSE,
    disconnectSSE,
    getChannelData,
    fetchChannels,
  };
});
