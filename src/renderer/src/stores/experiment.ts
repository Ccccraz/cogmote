import { ref } from 'vue'
import { defineStore } from 'pinia'
import ky from 'ky'

/**
 * experimentRecord
 */
export interface ExperimentRecord {
  /**
   * The current branch of the Git type repository
   */
  branch: null | string
  /**
   * Experiment meta-information
   */
  experiment: Experiment
  /**
   * Registration ID of experiment in cogmoteGO
   */
  id: string
  /**
   * Last update time
   */
  last_update: string
  /**
   * The time of registration to cogmoteGO
   */
  register_time: string
  /**
   * The status of the experiments repository
   */
  status: string
  [property: string]: unknown
}

/**
 * Experiment meta-information
 *
 * experiment
 */
export interface Experiment {
  /**
   * If it is a git repository, then the address of the repository is
   */
  address: null | string
  /**
   * Experimental data path
   */
  data_path: null | string
  /**
   * Commands that cogmoteGO is expected to execute when accessing the start port
   */
  execs: Exec[]
  /**
   * The name of the experiment registered to cogmoteGO
   */
  nickname: string
  /**
   * The existence form of experimental files
   */
  type: string
  [property: string]: unknown
}

export interface Exec {
  /**
   * Specific commands
   */
  exec: string
  /**
   * The name of the command
   */
  nickname: null | string
  [property: string]: unknown
}

export const useExperimentStore = defineStore('ExperimentStore', () => {
  const experimentRecords = ref<ExperimentRecord[]>([])

  const fetchExperiments = async (device_address: string): Promise<void> => {
    const url = `http://${device_address}:9012/api/exps`
    try {
      experimentRecords.value = await ky.get(url, { timeout: 1000 }).json<ExperimentRecord[]>()
      console.log('experimentRecords:', experimentRecords.value)
    } catch (err) {
      console.error('fetch experiment error:', err)
    }
  }

  return {
    experimentRecords,
    fetchExperiments
  }
})
