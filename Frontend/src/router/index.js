import Vue from 'vue'
import VueRouter from 'vue-router'
import { Auth } from 'aws-amplify';
// import { component } from 'vue/types/umd'
import LoginPage from '../views/LoginPage.vue'
import SignUpPage from '../views/SignUpPage.vue'
import SearchPage from '../views/SearchPage.vue'
import AccountPage from '../views/AccountPage.vue'
import HomePage from '../views/HomePage.vue'
import SocialPage from '../views/SocialPage.vue'
import FriendPage from '../views/FriendPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/signup',
    name: "SignUpPage",
    component: SignUpPage
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomePage,
    meta: {requiresAuth: true}
  },
  {
    path: '/search',
    name: "SearchPage",
    component: SearchPage,
    meta: {requiresAuth: true}
  },
  {
    path: '/friend',
    name: "FriendPage",
    component: FriendPage,
    meta: {requiresAuth: true}
  },
  {
    path: '/account',
    name: "AccountPage",
    component: AccountPage,
    meta: {requiresAuth: true}
  },
  {
    path: '/social',
    name: "SocialPage",
    component: SocialPage,
    meta: {requiresAuth: true}
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = await Auth.currentUserInfo();
  console.log(isAuthenticated);

  if (requiresAuth && !isAuthenticated) {
    next("/");
  } else if (isAuthenticated && !requiresAuth){
    next("/home")
  }
  else{
    next()
  }

})

export default router