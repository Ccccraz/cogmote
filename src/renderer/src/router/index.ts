import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import DataQuickJudgeView from '@/views/DataQuickJudgeView.vue'
import VideoMonitorView from '@/views/VideoMonitorView.vue'
import DeviceHomeView from '@/views/DeviceHomeView.vue'
import Dashboardview from '@/views/Dashboardview.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/device',
      name: 'device',
      component: DeviceHomeView,
      children: [
        {
          path: ':address',
          component: Dashboardview
        }
      ]
    },
    {
      path: '/quick-judge',
      name: 'quickJudge',
      component: DataQuickJudgeView
    },
    {
      path: '/monitor',
      name: 'monitor',
      component: VideoMonitorView
    }
  ]
})

export default router
