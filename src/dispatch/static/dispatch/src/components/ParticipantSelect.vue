<template>
  <v-autocomplete
    :items="items"
    :label="label"
    :loading="loading"
    v-model:search="search"
    clearable
    hide-selected
    item-title="individual.name"
    item-value="individual.id"
    return-object
    chips
    :hide-no-data="false"
    v-model="participant"
    @update:model-value="handleClear"
  >
    <template #no-data>
      <v-list-item v-if="!loading">
        <v-list-item-title>
          No individuals matching <strong>"{{ search }}".</strong>
        </v-list-item-title>
      </v-list-item>
    </template>
    <template #item="{ props, item }">
      <v-list-item v-bind="props" :subtitle="item.raw.individual.email" />
    </template>
    <template #append-item v-if="items.length < total.value">
      <v-list-item @click="loadMore()">
        <v-list-item-subtitle> Load More </v-list-item-subtitle>
      </v-list-item>
    </template>
    <template #chip="data">
      <v-chip v-bind="data.props" pill>
        <template #prepend>
          <v-avatar color="teal" start> {{ initials(data.item.title) }} </v-avatar>
        </template>
        {{ data.item.title }}
      </v-chip>
    </template>
  </v-autocomplete>
</template>

<script>
import { ref, watch, onMounted } from "vue"
import { initials } from "@/filters"
import { debounce } from "lodash"

import IndividualApi from "@/individual/api"

export default {
  name: "ParticipantSelect",
  props: {
    label: {
      type: String,
      default: "Participant",
    },
    initialValue: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props) {
    let loading = ref(false)
    let items = ref([])
    let numItems = ref(10)
    let participant = ref({ ...props.initialValue })
    let currentPage = ref(1)
    let total = ref(0)
    const search = ref(props.initialValue.name)

    let debouncedGetIndividualData = null

    const getIndividualData = async (searchVal, page = currentPage.value) => {
      loading.value = true
      let filterOptions = {
        q: searchVal,
        sortBy: ["name"],
        descending: [false],
        itemsPerPage: numItems.value * page,
      }

      await IndividualApi.getAll(filterOptions).then((response) => {
        items.value = response.data.items.map(function (x) {
          return { individual: x }
        })
        total.value = response.data.total
      })

      loading.value = false
    }

    onMounted(() => {
      debouncedGetIndividualData = debounce(getIndividualData, 300)
      debouncedGetIndividualData(search.value)
    })

    const loadMore = async () => {
      currentPage.value++
      numItems.value += 10
      await debouncedGetIndividualData(search.value)
    }

    const handleClear = (newValue) => {
      if (!newValue) {
        items.value = []
        search.value = null
        participant.value = null
        numItems.value = 10
        currentPage.value = 1
      }
    }

    watch(search, async (newVal, oldVal) => {
      if (oldVal !== newVal) {
        numItems.value = 10
        await debouncedGetIndividualData(newVal)
      }
    })

    return {
      getIndividualData,
      handleClear,
      initials,
      items,
      loading,
      loadMore,
      participant,
      search,
      total,
    }
  },
}
</script>
