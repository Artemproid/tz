import hexToRgba from './hex-to-rgba'
import { useForm, useFormWithValidation } from './validation'

export { 
  hexToRgba,
  useForm,
  useFormWithValidation
}

export const checkIfAuthorized = () => {
  const token = localStorage.getItem('token')
  return !!token
}

export const saveTokenToLocalStorage = (token) => {
  localStorage.setItem('token', token)
}

export const removeTokenFromLocalStorage = () => {
  localStorage.removeItem('token')
}