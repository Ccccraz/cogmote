<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Search, Loader2 } from "lucide-vue-next";
import { toast } from "vue-sonner";

import { useDeviceStore } from "@/stores/device";
import { computed, ref } from "vue";

const deviceStore = useDeviceStore();

const ipParts = ref<string[]>(["192", "168", "1", "*"]);

const ipList = computed(() => {
  return Array.from(
    { length: 255 },
    (_, i) =>
      `${ipParts.value[0]}.${ipParts.value[1]}.${ipParts.value[2]}.${i + 1}`
  );
});

const detect = async () => {
  await deviceStore.fetchDevices(ipList.value);
  if (deviceStore.numberOfDetectedDevices() > 0) {
    toast.success(`${deviceStore.numberOfDetectedDevices()} devices detected`);
  } else {
    toast.error("No devices detected");
  }
};
</script>

<template>
  <Dialog>
    <DialogTrigger as-child>
      <Button>
        <Search />
      </Button>
    </DialogTrigger>
    <DialogContent class="sm:max-w-[618px]">
      <DialogHeader>
        <DialogTitle>Detect cogmoteGO</DialogTitle>
        <DialogDescription>
          set the IP range to be automatically detected
        </DialogDescription>
      </DialogHeader>
      <div class="grid gap-4 py-4">
        <div class="grid grid-cols-5 items-center gap-4">
          <Label> Range: </Label>
          <template v-for="(part, index) in ipParts">
            <Input
              v-if="index !== 3"
              :id="`ip-part-${index}`"
              v-model="ipParts[index]"
              :default-value="`${part}`"
              type="number"
              maxlength="3"
            />
            <Input
              v-else
              disabled
              :id="`ip-part-${index}`"
              v-model="ipParts[index]"
              :default-value="`${part}`"
              type="text"
              class="text-center"
              maxlength="3"
            />
          </template>
        </div>
      </div>
      <DialogFooter>
        <Button @click="detect">
          <Loader2 class="animate-spin" v-if="deviceStore.loading" /> Detect
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
