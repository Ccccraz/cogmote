<script setup lang="ts">
import { useColorMode } from "@vueuse/core";

import { Toaster } from "@/components/ui/sonner";
import "vue-sonner/style.css"; // vue-sonner v2 requires this import
import { Home, Monitor, CheckCheck, Boxes } from "lucide-vue-next";

import { RouterView } from "vue-router";

import { useDeviceStore } from "@/stores/device";

const deviceStore = useDeviceStore();

const mode = useColorMode();
mode.value = "auto";
</script>

<template>
  <Toaster />
  <main class="flex flex-col h-screen w-screen bg-sidebar">
    <header class="h-10 w-full flex items-center justify-center p-2">
      <h1 class="text-sm font-medium tracking-wide">cogmote</h1>
    </header>

    <section class="flex-1 flex">
      <aside class="w-10">
        <nav class="flex flex-col items-center justify-center space-y-4 p-2">
          <RouterLink to="/">
            <Home class="text-muted-foreground" />
          </RouterLink>
          <RouterLink
            :to="`/device/${Array.from(deviceStore.devices.keys())[0]}`"
            :key="Array.from(deviceStore.devices.keys())[0]"
          >
            <Boxes class="text-muted-foreground" />
          </RouterLink>
          <RouterLink :to="'/quick-judge'">
            <CheckCheck class="text-muted-foreground" />
          </RouterLink>
          <RouterLink :to="'/monitor'">
            <Monitor class="text-muted-foreground" />
          </RouterLink>
          <!-- <RouterLink :to="'/test/127.0.0.1'">
            <Monitor class="text-muted-foreground" />
          </RouterLink> -->
        </nav>
      </aside>
      <main class="flex-1 flex bg-background rounded-xl border">
        <RouterView />
      </main>
    </section>
  </main>
</template>
