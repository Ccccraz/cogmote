/**
 * device
 */

export interface DeviceInfo {
  address: string
  status: string
  device: Device
}

export interface Device {
  arch: string
  hostname: string
  os: string
  uptime: number
  username: string
  cpu: string
  [property: string]: unknown
}
