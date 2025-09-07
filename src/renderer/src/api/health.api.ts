import { http } from '@/api/httpClient'
import { Device } from '@/types/device'

export async function getHealth(): Promise<Device> {
  const response = await http.get('/health')
  const data = response.json<Device>()
  return data
}
