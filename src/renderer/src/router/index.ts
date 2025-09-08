import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import DataQuickJudgeView from '@/views/DataQuickJudgeView.vue'
import VideoMonitorView from '@/views/VideoMonitorView.vue'
import DeviceHomeView from '@/views/DeviceHomeView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      component: HomeView
    },
    {
      path: '/device/:address',
      component: DeviceHomeView
    },
    {
      path: '/quick-judge',
      component: DataQuickJudgeView
    },
    {
      path: '/monitor',
      component: VideoMonitorView
    }
  ]
})

export default router
