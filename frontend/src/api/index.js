import { API_URL } from '../config'

const request = (endpoint, options = {}) => {
  return fetch(`${API_URL}${endpoint}`, {
    headers: {
      'content-type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  })
    .then(res => {
      if (res.ok) {
        return res.json()
      }
      return res.json().then(errorData => {
        const error = new Error('Request failed')
        error.status = res.status
        error.data = errorData
        error.message = Object.entries(errorData).map(([key, value]) => {
          if (Array.isArray(value)) {
            return `${key}: ${value.join(', ')}`
          }
          return `${key}: ${value}`
        }).join('; ')
        throw error
      })
    })
}

const requestWithAuth = (endpoint, options = {}) => {
  const token = localStorage.getItem('token')
  const hasBody = options.body !== undefined
  
  return request(endpoint, {
    ...options,
    headers: {
      'authorization': `Token ${token}`,
      // Принудительно устанавливаем Content-Type для запросов с телом
      ...(hasBody && { 'content-type': 'application/json' }),
      ...(options.headers || {})
    }
  })
}

const api = {
  // Auth endpoints
  signup: ({ email, username, first_name, last_name, password }) => request(`/api/auth/users/`, {
    method: 'POST',
    body: JSON.stringify({
      email,
      username,
      first_name,
      last_name,
      password
    })
  }),
  signin: ({ email, password }) => request(`/api/auth/token/login/`, {
    method: 'POST',
    body: JSON.stringify({
      email, password
    })
  }),
  signout: () => {
    const token = localStorage.getItem('token')
    const authorization = token ? { 'authorization': `Token ${token}` } : {}
    return request(`/api/auth/token/logout/`, {
      method: 'POST',
      headers: authorization
    })
  },
  // User management
  getUserData: () => requestWithAuth(`/api/v1/users/me/`),
  changePassword: ({ new_password, current_password }) => {
    const token = localStorage.getItem('token')
    return request(`/api/auth/users/set_password/`, {
      method: 'POST',
      headers: {
        'authorization': `Token ${token}`
      },
      body: JSON.stringify({ new_password, current_password })
    })
  },
  changeAvatar: (data) => {
    const token = localStorage.getItem('token')
    return fetch(`${API_URL}/api/v1/users/me/avatar/`, {
      method: 'PUT',
      headers: {
        'authorization': `Token ${token}`
      },
      body: data
    }).then(res => {
      if (res.ok) {
        return res.json()
      }
      return Promise.reject(res)
    })
  },
  deleteAvatar: () => {
    const token = localStorage.getItem('token')
    return fetch(`${API_URL}/api/v1/users/me/avatar/`, {
      method: 'DELETE',
      headers: {
        'authorization': `Token ${token}`
      }
    })
  },
  resetPassword: ({ email }) => request(`/api/auth/users/reset_password/`, {
    method: 'POST',
    body: JSON.stringify({ email })
  }),
  // User profiles and subscriptions
  getUser: ({ id }) => requestWithAuth(`/api/v1/users/${id}/`),
  getUsers: ({ page, limit }) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    if (limit) params.append('limit', limit)
    return requestWithAuth(`/api/v1/users/?${params.toString()}`)
  },
  getSubscriptions: ({ page, recipes_limit }) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    if (recipes_limit) params.append('recipes_limit', recipes_limit)
    return requestWithAuth(`/api/v1/users/subscriptions/?${params.toString()}`)
  },
  deleteSubscriptions: ({ id }) => requestWithAuth(`/api/v1/users/${id}/subscribe/`, {
    method: 'DELETE'
  }),
  subscribe: ({ id }) => requestWithAuth(`/api/v1/users/${id}/subscribe/`, {
    method: 'POST'
  }),

  // Reference data - user-specific
  getStatuses: ({ page } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    return requestWithAuth(`/api/v1/my/statuses/?${params.toString()}`)
  },
  createStatus: (data) => requestWithAuth(`/api/v1/my/statuses/`, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  updateStatus: ({ id, ...data }) => requestWithAuth(`/api/v1/my/statuses/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  deleteStatus: ({ id }) => requestWithAuth(`/api/v1/my/statuses/${id}/`, {
    method: 'DELETE'
  }),

  getTypes: ({ page } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    return requestWithAuth(`/api/v1/my/types/?${params.toString()}`)
  },
  createType: (data) => requestWithAuth(`/api/v1/my/types/`, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  updateType: ({ id, ...data }) => requestWithAuth(`/api/v1/my/types/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  deleteType: ({ id }) => requestWithAuth(`/api/v1/my/types/${id}/`, {
    method: 'DELETE'
  }),

  getCategories: ({ page, type } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    if (type) params.append('type', type)
    return requestWithAuth(`/api/v1/my/categories/?${params.toString()}`)
  },
  createCategory: (data) => requestWithAuth(`/api/v1/my/categories/`, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  updateCategory: ({ id, ...data }) => requestWithAuth(`/api/v1/my/categories/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  deleteCategory: ({ id }) => requestWithAuth(`/api/v1/my/categories/${id}/`, {
    method: 'DELETE'
  }),

  getSubcategories: ({ page, category } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    if (category) params.append('category', category)
    return requestWithAuth(`/api/v1/my/subcategories/?${params.toString()}`)
  },
  createSubcategory: (data) => requestWithAuth(`/api/v1/my/subcategories/`, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  updateSubcategory: ({ id, ...data }) => requestWithAuth(`/api/v1/my/subcategories/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  deleteSubcategory: ({ id }) => requestWithAuth(`/api/v1/my/subcategories/${id}/`, {
    method: 'DELETE'
  }),

  // Money flows
  getMoneyFlow: ({ id }) => requestWithAuth(`/api/v1/money-flows/${id}/`),
  getMoneyFlows: ({ page, ...filters } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        params.append(key, value)
      }
    })
    return requestWithAuth(`/api/v1/money-flows/?${params.toString()}`)
  },
  createMoneyFlow: (data) => requestWithAuth(`/api/v1/money-flows/`, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  updateMoneyFlow: ({ id, ...data }) => requestWithAuth(`/api/v1/money-flows/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  deleteMoneyFlow: ({ id }) => requestWithAuth(`/api/v1/money-flows/${id}/`, {
    method: 'DELETE'
  }),

  // Global reference data for selecting
  getAllStatuses: ({ page } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    return request(`/api/v1/statuses/?${params.toString()}`)
  },
  getAllTypes: ({ page } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    return request(`/api/v1/types/?${params.toString()}`)
  },
  getAllCategories: ({ page, type } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    if (type) params.append('type', type)
    return request(`/api/v1/categories/?${params.toString()}`)
  },
  getAllSubcategories: ({ page, category } = {}) => {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    if (category) params.append('category', category)
    return request(`/api/v1/subcategories/?${params.toString()}`)
  }
}

export default api
