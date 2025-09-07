import { useDeviceStore } from '@/stores/device'
import { toast } from 'vue-sonner'

interface DetectDevicesProps {
  genIpList(ipParts: string[]): string[]
  genDomainList(domainParts: string[]): string[]
  detect(ipList: string[]): Promise<boolean | void>
  detectDomain(domainList: string[]): Promise<boolean | void>
}

export function useDetectDevices(): DetectDevicesProps {
  const deviceStore = useDeviceStore()

  const genIpList = (ipParts: string[]): string[] => {
    const [part1, part2, part3, part4] = ipParts

    const validatePart = (part: string): boolean => {
      if (part === '*') return true
      const num = parseInt(part, 10)
      return !isNaN(num) && num >= 0 && num <= 255
    }

    if (
      !validatePart(part1) ||
      !validatePart(part2) ||
      !validatePart(part3) ||
      !validatePart(part4)
    ) {
      console.error("Invalid IP part: must be a number between 0-255 or '*'")
      return []
    }

    if (part3 === '*' && part4 === '*') {
      return Array.from({ length: 256 * 256 }, (_, i) => {
        const third = Math.floor(i / 256)
        const fourth = i % 256
        return `${part1}.${part2}.${third}.${fourth}`
      })
    } else if (part4 === '*') {
      return Array.from({ length: 256 }, (_, i) => {
        return `${part1}.${part2}.${part3}.${i}`
      })
    }

    return [`${part1}.${part2}.${part3}.${part4}`]
  }

  const genDomainList = (domainParts: string[]): string[] => {
    const [part1, part2, part3] = domainParts

    const validatePart = (part: string): boolean => {
      return part !== ''
    }

    if (!validatePart(part1) || !validatePart(part2) || !validatePart(part3)) {
      console.error('Invalid domain part: must be a non-empty string')
      return []
    }

    return Array.from({ length: parseInt(part2) }, (_, i) => {
      return `${part1}${i}.${part3}`
    })
  }

  const detect = async (ipList: string[]): Promise<boolean | void> => {
    await deviceStore.fetchDevices(ipList)
    showDetectionResult()
  }

  const detectDomain = async (domainList: string[]): Promise<boolean | void> => {
    await deviceStore.fetchDevices(domainList)
    showDetectionResult()
  }

  const showDetectionResult = (): void => {
    if (deviceStore.numberOfDetectedDevices() > 0) {
      toast.success(`${deviceStore.numberOfDetectedDevices()} devices detected`)
    } else {
      toast.error('No devices detected')
    }
  }

  return {
    genIpList,
    genDomainList,
    detect,
    detectDomain
  }
}
