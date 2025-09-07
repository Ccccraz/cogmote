import { app } from 'electron'
import { access, mkdir, readFile, writeFile } from 'node:fs/promises'
import { constants } from 'node:fs'
import { dirname } from 'node:path'
import { join } from 'node:path'

export function joinPath(...paths: string[]): string {
  return join(...paths)
}

export async function getAppdataPath(): Promise<string> {
  return app.getPath('appData')
}

export async function exists(path: string): Promise<boolean> {
  try {
    await access(path, constants.F_OK)
    return true
  } catch (error) {
    console.error(error)
    return false
  }
}

export async function createRecursive(path: string): Promise<boolean> {
  try {
    await mkdir(path, { recursive: true })
    return true
  } catch (error) {
    console.error(error)
    return false
  }
}

export async function readJsonFile(path: string): Promise<string | null> {
  try {
    return await readFile(path, 'utf-8')
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function writeJsonFile(path: string, data: string): Promise<boolean> {
  try {
    const dir = dirname(path)
    await createRecursive(dir)

    await writeFile(path, data, 'utf-8')
    return true
  } catch (error) {
    console.error(error)
    return false
  }
}

export const api = {
  joinPath,
  getAppdataPath,
  exists,
  createRecursive,
  readJsonFile,
  writeJsonFile
}
