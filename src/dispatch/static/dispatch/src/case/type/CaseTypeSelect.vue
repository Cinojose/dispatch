<template>
  <v-combobox
    v-model="case_type"
    :items="items"
    v-model:search="search"
    :menu-props="{ maxHeight: '400' }"
    item-title="name"
    item-value="id"
    :label="label"
    placeholder="Start typing to search"
    :hint="hint"
    return-object
    :loading="loading"
    no-filter
  >
    <template #item="data">
      <v-list-item v-bind="data.props" :title="null">
        <v-list-item-title>{{ data.item.raw.name }}</v-list-item-title>
        <v-list-item-subtitle :title="data.item.raw.description">
          {{ data.item.raw.description }}
        </v-list-item-subtitle>
      </v-list-item>
    </template>
    <template #append-item>
      <v-list-item v-if="more" @click="loadMore()">
        <v-list-item-subtitle> Load More </v-list-item-subtitle>
      </v-list-item>
    </template>
  </v-combobox>
</template>

<script>
import { cloneDeep } from "lodash"

import SearchUtils from "@/search/utils"
import CaseTypeApi from "@/case/type/api"

export default {
  name: "CaseTypeSelect",

  props: {
    modelValue: {
      type: Object,
      default: function () {
        return {}
      },
    },
    project: {
      type: [Object],
      default: null,
    },
    hint: {
      type: String,
      default: function () {
        return "Case Type to associate"
      },
    },
    label: {
      type: String,
      default: function () {
        return "Case Type"
      },
    },
  },

  data() {
    return {
      loading: false,
      items: [],
      search: null,
      more: false,
      numItems: 5,
    }
  },

  computed: {
    case_type: {
      get() {
        return cloneDeep(this.modelValue)
      },
      set(value) {
        this.$emit("update:modelValue", value)
      },
    },
  },

  methods: {
    loadMore() {
      this.numItems = this.numItems + 5
      this.fetchData()
    },
    fetchData() {
      this.error = null
      this.loading = "error"

      let filterOptions = {
        q: this.search,
        sortBy: ["name"],
        descending: [false],
        itemsPerPage: this.numItems,
      }

      if (this.project) {
        filterOptions = {
          ...filterOptions,
          filters: {
            project: [this.project],
            enabled: ["true"],
          },
        }
      }

      filterOptions = SearchUtils.createParametersFromTableOptions({ ...filterOptions })

      CaseTypeApi.getAll(filterOptions).then((response) => {
        this.items = response.data.items

        if (this.case_type) {
          // check to see if the current selection is available in the list and if not we add it
          if (!this.items.find((match) => match.id === this.case_type.id)) {
            this.items = [this.case_type].concat(this.items)
          }
        }

        this.total = response.data.total
        this.loading = false

        if (this.items.length < this.total) {
          this.more = true
        } else {
          this.more = false
        }
      })
    },
  },

  watch: {
    search(val) {
      val && val !== this.select && this.fetchData()
    },
    value(val) {
      if (!val) return
      this.items.push(val)
    },
  },

  created() {
    this.fetchData()
    this.$watch(
      (vm) => [vm.project],
      () => {
        this.fetchData()
      }
    )
  },
}
</script>
