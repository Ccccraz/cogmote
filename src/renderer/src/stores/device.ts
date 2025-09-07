import { Ref, ref } from 'vue'
import { defineStore } from 'pinia'
import type { DeviceInfo, Device } from '@/types/device'
import ky from 'ky'

export const useDeviceStore = defineStore('devices', () => {
  const devices: Ref<Map<string, DeviceInfo>> = ref<Map<string, DeviceInfo>>(new Map())
  const loading: Ref<boolean> = ref(false)
  const detectedDevices: Ref<number> = ref(0)
  let appdataPath: string = ''
  let devicesDataPath: string = ''

  const initlize = async (): Promise<boolean | void> => {
    appdataPath = await window.ipcApi.fsApi.getAppdataPath()
    devicesDataPath = await window.ipcApi.fsApi.joinPath(appdataPath, 'cogmote', 'devices.json')

    const ifDirectoriesExist = await window.ipcApi.fsApi.exists(appdataPath)

    if (!ifDirectoriesExist) {
      await window.ipcApi.fsApi.createRecursive(appdataPath)
    }

    const ifFileExists = await window.ipcApi.fsApi.exists(devicesDataPath)

    if (!ifFileExists) {
      await window.ipcApi.fsApi.writeJsonFile(devicesDataPath, JSON.stringify([]))
      return
    }

    try {
      const devicesRaw = await window.ipcApi.fsApi.readJsonFile(devicesDataPath)
      const devicesJson = JSON.parse(devicesRaw || '[]')

      devicesJson.forEach((deviceInfo: DeviceInfo) => {
        if (deviceInfo.address && deviceInfo.device) {
          devices.value.set(deviceInfo.address, deviceInfo)
        }
      })

      await Promise.all(
        Array.from(devices.value.values()).map((deviceInfo: DeviceInfo) =>
          _reconnectDevice(deviceInfo)
        )
      )

      await saveDevicesToFile()
    } catch (err) {
      console.error('Error reading devices.json:', err)

      await window.ipcApi.fsApi.writeJsonFile(devicesDataPath, JSON.stringify([]))
    }
  }

  const saveDevicesToFile = async (): Promise<boolean | void> => {
    try {
      const devicesArray = Array.from(devices.value.values())
      await window.ipcApi.fsApi.writeJsonFile(
        devicesDataPath,
        JSON.stringify(devicesArray, null, 2)
      )
    } catch (err) {
      console.error('Error saving devices to file:', err)
    }
  }

  const reconnectDevice = async (): Promise<void> => {
    await Promise.all(
      Array.from(devices.value.values()).map((deviceInfo: DeviceInfo) =>
        _reconnectDevice(deviceInfo)
      )
    )
  }

  const _reconnectDevice = async (device: DeviceInfo): Promise<void> => {
    try {
      const currentDevice = await fetchDevice(device.address)
      if (currentDevice) {
        devices.value.set(device.address, {
          ...currentDevice,
          status: 'online'
        })
      } else {
        devices.value.set(device.address, {
          ...device,
          status: 'offline'
        })
      }
    } catch (err) {
      console.log(err)
      devices.value.set(device.address, {
        ...device,
        status: 'offline'
      })
    }
  }

  const addDevice = async (address: string): Promise<void> => {
    loading.value = true
    const device = await fetchDevice(address)
    if (device) {
      devices.value.set(address, device)
    }
    loading.value = false
  }

  const fetchDevice = async (address: string): Promise<DeviceInfo | null> => {
    try {
      const device = await ky
        .get(`http://${address}:9012/api/device`, {
          timeout: 1000
        })
        .json<Device>()
      const deviceInfo: DeviceInfo = {
        status: 'online',
        address: address,
        device: device
      }
      return deviceInfo
    } catch (err) {
      console.log('Error fetching device:', err)
      return null
    }
  }

  const fetchDevices = async (addresses: string[]): Promise<boolean | void> => {
    loading.value = true
    detectedDevices.value = 0
    try {
      await Promise.all(
        addresses.map(async (address) => {
          const device = await fetchDevice(address)
          if (device) {
            detectedDevices.value++
            devices.value.set(address, device)
            return { address, device }
          }
          return null
        })
      )
      await saveDevicesToFile()
    } catch (err) {
      console.log('Error fetching devices:', err)
    } finally {
      loading.value = false
    }
  }

  const getDevice = (address: string): DeviceInfo | undefined => {
    return devices.value.get(address)
  }

  const numberOfDetectedDevices = (): number => {
    return detectedDevices.value
  }

  initlize()

  return {
    devices,
    reconnectDevice,
    addDevice,
    fetchDevices,
    loading,
    numberOfDetectedDevices,
    getDevice
  }
})
