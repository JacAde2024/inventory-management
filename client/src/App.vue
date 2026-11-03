<template>
  <div class="app">
    <button class="sidebar-toggle" @click="sidebarOpen = !sidebarOpen" aria-label="Toggle navigation">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>

    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-brand">
        <div class="brand-mark">{{ t('nav.companyName').slice(0, 2).toUpperCase() }}</div>
        <div class="brand-text">
          <span class="brand-name">{{ t('nav.companyName') }}</span>
          <span class="brand-subtitle">{{ t('nav.subtitle') }}</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }" @click="sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg></span>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </router-link>
        <router-link to="/inventory" class="nav-item" :class="{ active: $route.path === '/inventory' }" @click="sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/></svg></span>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </router-link>
        <router-link to="/orders" class="nav-item" :class="{ active: $route.path === '/orders' }" @click="sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 2h6v3H9z"/><path d="M8 10h8M8 14h8M8 18h5"/></svg></span>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </router-link>
        <router-link to="/restocking" class="nav-item" :class="{ active: $route.path === '/restocking' }" @click="sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 15.3-6.4L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15.3 6.4L3 16"/><path d="M3 21v-5h5"/></svg></span>
          <span class="nav-label">{{ t('nav.restocking') }}</span>
        </router-link>
        <router-link to="/spending" class="nav-item" :class="{ active: $route.path === '/spending' }" @click="sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 10v.01M18 14v.01"/></svg></span>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </router-link>
        <router-link to="/demand" class="nav-item" :class="{ active: $route.path === '/demand' }" @click="sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 7-8"/><path d="M15 7h5v5"/></svg></span>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </router-link>
        <router-link to="/reports" class="nav-item" :class="{ active: $route.path === '/reports' }" @click="sidebarOpen = false">
          <span class="nav-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg></span>
          <span class="nav-label">{{ t('nav.reports') }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <LanguageSwitcher />
      </div>
    </aside>

    <div class="app-shell">
      <header class="topbar">
        <FilterBar />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </header>
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal :is-open="showProfileDetails" @close="showProfileDetails = false" />
    <TasksModal :is-open="showTasks" :tasks="tasks" @close="showTasks = false" @add-task="addTask" @delete-task="deleteTask" @toggle-task="toggleTask" />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const sidebarOpen = ref(false)
    const apiTasks = ref([])

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(loadTasks)

    return {
      t,
      showProfileDetails,
      showTasks,
      sidebarOpen,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
:root {
  --accent-50: #eef2ff;
  --accent-100: #e0e7ff;
  --accent-500: #6366f1;
  --accent-600: #4f46e5;
  --accent-700: #4338ca;

  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;

  --success: #059669;
  --success-bg: #d1fae5;
  --warning: #d97706;
  --warning-bg: #fed7aa;
  --danger: #dc2626;
  --danger-bg: #fecaca;
  --info: var(--accent-600);
  --info-bg: var(--accent-100);

  --surface: #ffffff;
  --surface-sunken: var(--gray-50);
  --border: var(--gray-200);
  --text-primary: var(--gray-900);
  --text-secondary: var(--gray-500);

  --sidebar-bg: #111827;
  --sidebar-text: #9ca3af;
  --sidebar-text-active: #ffffff;
  --sidebar-active-bg: rgba(99, 102, 241, 0.16);
  --sidebar-border: rgba(255, 255, 255, 0.08);
  --sidebar-width: 264px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-8: 48px;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-pill: 999px;

  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);
  --shadow-lg: 0 12px 32px rgba(15, 23, 42, 0.12);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--surface-sunken);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  display: flex;
  min-height: 100vh;
  background: var(--surface-sunken);
}

.sidebar-toggle {
  display: none;
  position: fixed;
  top: var(--space-3);
  left: var(--space-3);
  z-index: 210;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-primary);
  align-items: center;
  justify-content: center;
}
.sidebar-toggle svg { width: 20px; height: 20px; }

.sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  background: var(--sidebar-bg);
  display: flex;
  flex-direction: column;
  padding: var(--space-5) var(--space-3);
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 0 var(--space-3) var(--space-5);
  margin-bottom: var(--space-3);
  border-bottom: 1px solid var(--sidebar-border);
}

.brand-mark {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--accent-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.brand-text { display: flex; flex-direction: column; min-width: 0; }
.brand-name { color: white; font-weight: 700; font-size: 0.938rem; letter-spacing: -0.01em; white-space: nowrap; }
.brand-subtitle { color: var(--sidebar-text); font-size: 0.75rem; }

.sidebar-nav { display: flex; flex-direction: column; gap: 2px; flex: 1; }

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-md);
  color: var(--sidebar-text);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  position: relative;
  transition: background 0.15s ease, color 0.15s ease;
}
.nav-item:hover { background: rgba(255, 255, 255, 0.04); color: white; }
.nav-item.active { background: var(--sidebar-active-bg); color: var(--sidebar-text-active); }
.nav-item.active::before {
  content: '';
  position: absolute;
  left: -12px;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: var(--accent-500);
  border-radius: var(--radius-pill);
}

.nav-icon { width: 20px; height: 20px; flex-shrink: 0; display: flex; }
.nav-icon svg { width: 100%; height: 100%; }

.sidebar-footer { padding-top: var(--space-4); border-top: 1px solid var(--sidebar-border); }

.app-shell { flex: 1; display: flex; flex-direction: column; min-width: 0; }

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-6);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 50;
}

.main-content {
  flex: 1;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-6);
}

@media (max-width: 900px) {
  .sidebar-toggle { display: flex; }
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    transform: translateX(-100%);
    z-index: 200;
    transition: transform 0.2s ease;
    box-shadow: var(--shadow-lg);
  }
  .sidebar.open { transform: translateX(0); }
  .topbar { padding-left: var(--space-8); }
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.375rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: var(--text-secondary);
  font-size: 0.938rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-5);
  margin-bottom: var(--space-6);
}

.stat-card {
  background: var(--surface);
  padding: var(--space-5);
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: var(--gray-300);
  box-shadow: var(--shadow-md);
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: var(--warning);
}

.stat-card.success .stat-value {
  color: var(--success);
}

.stat-card.danger .stat-value {
  color: var(--danger);
}

.stat-card.info .stat-value {
  color: var(--info);
}

.card {
  background: var(--surface);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  border: 1px solid var(--border);
  margin-bottom: var(--space-5);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.875rem;
  border-bottom: 1px solid var(--border);
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--gray-50);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

th {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font-weight: 600;
  color: var(--gray-600);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid var(--gray-100);
  color: var(--text-secondary);
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: var(--gray-50);
}

.badge {
  display: inline-block;
  padding: 0.313rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: var(--success-bg);
  color: var(--success);
}

.badge.warning {
  background: var(--warning-bg);
  color: var(--warning);
}

.badge.danger {
  background: var(--danger-bg);
  color: var(--danger);
}

.badge.info {
  background: var(--info-bg);
  color: var(--info);
}

.badge.increasing {
  background: var(--success-bg);
  color: var(--success);
}

.badge.decreasing {
  background: var(--danger-bg);
  color: var(--danger);
}

.badge.stable {
  background: var(--accent-100);
  color: var(--accent-700);
}

.badge.high {
  background: var(--danger-bg);
  color: var(--danger);
}

.badge.medium {
  background: var(--warning-bg);
  color: var(--warning);
}

.badge.low {
  background: var(--info-bg);
  color: var(--info);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid var(--danger-bg);
  color: var(--danger);
  padding: 1rem;
  border-radius: var(--radius-sm);
  margin: 1rem 0;
  font-size: 0.938rem;
}
</style>
