import { contextBridge } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'
import { fsApi } from './fs_utils'

interface IpcApi {
  fsApi: typeof fsApi
}

const ipcApi: IpcApi = {
  fsApi: fsApi
}

// Use `contextBridge` APIs to expose Electron APIs to
// renderer only if context isolation is enabled, otherwise
// just add to the DOM global.
if (process.contextIsolated) {
  try {
    contextBridge.exposeInMainWorld('electron', electronAPI)
    contextBridge.exposeInMainWorld('ipcApi', ipcApi)
  } catch (error) {
    console.error(error)
  }
} else {
  // @ts-ignore (define in dts)
  window.electron = electronAPI
  // @ts-ignore (define in dts)
  window.api = api
}
