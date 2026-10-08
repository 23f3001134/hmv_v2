<template>
  <div class="card border-0 shadow-sm h-100">
    <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
      <div>
        <h5 class="mb-0">Doctor Availability</h5>
        <small class="text-muted">Set time slots so patients can book.</small>
      </div>
      <span class="badge text-bg-primary">Weekly</span>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table align-middle">
          <thead class="table-light">
            <tr>
              <th style="width: 160px;">Date</th>
              <th>Morning Slot</th>
              <th>Evening Slot</th>
              <th style="width: 90px;">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="availability.length === 0">
              <td colspan="4" class="text-center text-muted py-3">
                No availability set yet. Add your first row below.
              </td>
            </tr>
            <tr v-for="(slot, index) in availability" :key="`${slot.date}-${index}`">
              <td>
                <input v-model="slot.date" class="form-control" type="date" />
              </td>
              <td>
                <input
                  v-model="slot.morning_slot"
                  class="form-control"
                  type="text"
                  placeholder="08:00 - 12:00"
                />
              </td>
              <td>
                <input
                  v-model="slot.evening_slot"
                  class="form-control"
                  type="text"
                  placeholder="04:00 - 09:00"
                />
              </td>
              <td>
                <button class="btn btn-outline-danger btn-sm" @click="$emit('remove-row', index)">
                  Remove
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center gap-2">
        <p class="text-muted small mb-0">
          Keep your slots updated so patients can book without delays.
        </p>
        <div class="d-flex gap-2">
          <button class="btn btn-outline-primary" @click="$emit('add-row')">
            + Add Row
          </button>
          <button class="btn btn-primary" @click="$emit('save')" :disabled="saving">
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  availability: { type: Array, default: () => [] },
  saving: { type: Boolean, default: false }
})

defineEmits(["save", "add-row", "remove-row"])
</script>
