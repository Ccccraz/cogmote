<script setup lang="ts">
import {
  Card,
  CardContent,
  CardTitle,
  CardHeader,
  CardDescription,
  CardFooter,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { DeviceInfo } from "@/types/device";

defineProps<{
  address: string;
  device: DeviceInfo;
}>();

</script>

<template>
  <Card
    class="min-w-auto w-80 h-fit transition-all hover:shadow-white/20 bg-muted/50"
  >
    <CardHeader>
      <div class="flex justify-between">
        <CardTitle>{{ device.device.hostname }}</CardTitle>
        <Badge v-if="device.status === 'online'" class="bg-green-300">{{ device.status }}</Badge>
        <Badge v-else="device.status === 'offline'" class="bg-red-300">{{ device.status }}</Badge>
      </div>
      <CardDescription>Last online: 1 day</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="flex justify-between">
        <Label>Address: </Label>
        <Label> {{ address }}</Label>
      </div>
    </CardContent>
    <CardFooter class="flex justify-between">
      <Button>Detial</Button>
      <Button>Link</Button>
    </CardFooter>
  </Card>
</template>
