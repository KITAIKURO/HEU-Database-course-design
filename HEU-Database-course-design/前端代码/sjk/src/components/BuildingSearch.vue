<template>
  <div class="search-page">
    <el-card class="search-card" shadow="hover">
      <h2 class="title">楼宇信息查询</h2>
      <p class="subtitle">根据楼宇名称关键字查询面积、租金与空置率。</p>
      <el-form :inline="true" @submit.native.prevent="onSearch" class="search-form">
        <el-form-item label="楼宇名称">
          <el-input
            v-model="keyword"
            placeholder="请输入楼宇名称关键字"
            clearable
            @keyup.enter.native="onSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch">查询</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>

      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        closable
        @close="errorMessage = ''"
        class="alert"
      />

      <el-table
        v-if="results.length"
        :data="results"
        border
        stripe
        style="width: 100%"
        class="result-table"
      >
        <el-table-column prop="building_name" label="楼宇名称" min-width="200" />
        <el-table-column prop="area_sqm" label="面积(㎡)" width="120" />
        <el-table-column prop="asking_rent_mb_per_spm_month" label="表面租金(元/㎡·月)" width="180" />
        <el-table-column prop="effective_rent_mb_per_spm_month" label="有效租金(元/㎡·月)" width="180" />
        <el-table-column prop="vacancy_rate" label="空置率(%)" width="120" />
      </el-table>
      <el-empty
        v-else
        description="请先输入楼宇名称进行查询"
        :image-size="120"
      />
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'BuildingSearch',
  data() {
    return {
      keyword: '',
      results: [],
      errorMessage: ''
    }
  },
  methods: {
    async onSearch() {
      this.errorMessage = ''
      if (!this.keyword.trim()) {
        this.errorMessage = '请输入要查询的楼宇名称'
        this.results = []
        return
      }

      try {
        const { data } = await this.$axios.get('/api/buildings/search', {
          params: { name: this.keyword }
        })

        if (data.code === 200) {
          this.results = data.data
          if (!data.data.length) {
            this.errorMessage = '没有找到匹配的楼宇，请尝试其他关键字。'
          }
        } else {
          this.errorMessage = data.msg || '查询失败，请稍后重试。'
          this.results = []
        }
      } catch (error) {
        console.error(error)
        this.errorMessage = '查询过程中出现问题，请稍后重试。'
        this.results = []
      }
    },
    resetForm() {
      this.keyword = ''
      this.results = []
      this.errorMessage = ''
    }
  }
}
</script>

<style scoped>
.search-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 16px;
  background: #f5f7fa;
  min-height: 100vh;
  box-sizing: border-box;
}

.search-card {
  width: 100%;
  max-width: 1080px;
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  margin: 8px 0 24px;
  color: #606266;
}

.search-form {
  margin-bottom: 12px;
}

.alert {
  margin-bottom: 12px;
}

.result-table {
  margin-top: 12px;
}
</style>
