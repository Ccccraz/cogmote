import { ipcRenderer } from 'electron/renderer'

export const fsApi = {
  joinPath: async (...paths: string[]): Promise<string> => ipcRenderer.invoke('joinPath', ...paths),
  getAppdataPath: async (): Promise<string> => ipcRenderer.invoke('getAppdataPath'),
  exists: async (path: string): Promise<boolean> => ipcRenderer.invoke('exists', path),
  createRecursive: async (path: string): Promise<boolean> =>
    ipcRenderer.invoke('createRecursive', path),
  readJsonFile: async (path: string): Promise<string | null> =>
    ipcRenderer.invoke('readJsonFile', path),
  writeJsonFile: async (path: string, data: string): Promise<boolean> =>
    ipcRenderer.invoke('writeJsonFile', path, data)
}
