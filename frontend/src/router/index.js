import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/users'

import HomeView from '@/views/HomeView.vue'
import NotFound from '@/components/NotFound.vue'
import CompareListView from '@/views/CompareListView.vue'
import DepositList from '@/components/DepositList.vue'
import SavingList from '@/components/SavingList.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import MapView from '@/views/MapView.vue'
import ArticleListView from '@/views/ArticleListView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import SignInView from '@/views/SignInView.vue'
import MyPageView from '@/views/MyPageView.vue'
import Profile from '@/components/Profile.vue'
import ProductManage from '@/components/ProductManage.vue'
import ProductRecommend from '@/components/ProductRecommend.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/compare',
      component: CompareListView,
      children: [
        {
          path: 'deposit',
          name: 'depositList',
          component: DepositList
        },
        {
          path: 'saving',
          name: 'savingList',
          component: SavingList
        }
      ]
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView
    },
    {
      path: '/bank',
      name: 'map',
      component: MapView
    },
    {
      path: '/articles',
      name: 'articleList',
      component: ArticleListView
    },
    {
      path: '/articles/:id',
      name: 'articleDetail',
      component: ArticleDetailView
    },
    {
      path: '/articles/create',
      name: 'articleCreate',
      component: ArticleCreateView
    },
    {
      path: '/articles/:id/update',
      name: 'articleUpdate',
      component: ArticleUpdateView
    },
    {
      path: '/signup',
      name: 'signUp',
      component: SignUpView
    },
    {
      path: '/signin',
      name: 'signIn',
      component: SignInView
    },
    {
      path: '/mypage/:username*',
      component: MyPageView,
      children: [
        {
          path: 'profile',
          name: 'profile',
          component: Profile
        },
        {
          path: 'manage',
          name: 'productManage',
          component: ProductManage
        },
        {
          path: 'recommend',
          name: 'productRecommend',
          component: ProductRecommend
        }
      ]
    },
    {
      path: '/404',
      name: 'notFound',
      component: NotFound
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404'
    }
  ]
})

router.beforeEach((to, from, next) => {
  const store = useUserStore()
  const authRequiredPages = ['articleList', 'articleDetail', 'articleCreate', 'articleUpdate', 'profile', 'productManage', 'productRecommend']
  const authRequired = authRequiredPages.includes(to.name)

  if (authRequired && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return next({ name: 'signIn' })
  }

  if ((to.name === 'signUp' || to.name === 'signIn') && store.isLogin) {
    window.alert('이미 로그인 했습니다.')
    return next({ name: 'home' })
  }

  next()
})

export default router