import Vue from 'vue'
import VueRouter from 'vue-router'
import BuildingSearch from '@/components/BuildingSearch'
Vue.use(VueRouter)
export default new VueRouter({
    mode:'history',
    routes: [
        {
            path:'/',
            component: BuildingSearch,
            meta: {
                title: "楼宇信息查询"
            }
        },
    ]
})