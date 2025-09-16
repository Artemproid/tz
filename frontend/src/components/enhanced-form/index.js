import React from 'react';
import { useForm } from '../../hooks/useApi';
import styles from './styles.module.css';

const FormField = ({ 
  type = 'text', 
  name, 
  label, 
  value, 
  error, 
  touched, 
  onChange, 
  onBlur, 
  required = false,
  placeholder,
  options = [], // для select
  ...props 
}) => {
  const fieldId = `field-${name}`;
  const hasError = touched && error;

  const handleChange = (e) => {
    const newValue = type === 'checkbox' ? e.target.checked : e.target.value;
    onChange(name, newValue);
  };

  const handleBlur = () => {
    onBlur(name);
  };

  const renderInput = () => {
    const commonProps = {
      id: fieldId,
      name,
      value: value || '',
      onChange: handleChange,
      onBlur: handleBlur,
      className: `${styles.input} ${hasError ? styles.inputError : ''}`,
      placeholder,
      ...props
    };

    switch (type) {
      case 'textarea':
        return <textarea {...commonProps} />;
      
      case 'select':
        return (
          <select {...commonProps}>
            <option value="">Выберите...</option>
            {options.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );
      
      case 'checkbox':
        return (
          <input
            {...commonProps}
            type="checkbox"
            checked={value || false}
            className={styles.checkbox}
          />
        );
      
      case 'file':
        return (
          <input
            {...commonProps}
            type="file"
            onChange={(e) => onChange(name, e.target.files[0])}
            className={styles.fileInput}
          />
        );
      
      default:
        return <input {...commonProps} type={type} />;
    }
  };

  return (
    <div className={styles.fieldContainer}>
      <label htmlFor={fieldId} className={styles.label}>
        {label}
        {required && <span className={styles.required}>*</span>}
      </label>
      {renderInput()}
      {hasError && <div className={styles.errorMessage}>{error}</div>}
    </div>
  );
};

const EnhancedForm = ({ 
  initialValues = {}, 
  onSubmit, 
  validate,
  fields = [],
  submitText = 'Отправить',
  children,
  className = ''
}) => {
  const {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    reset
  } = useForm(initialValues, onSubmit, validate);

  return (
    <form 
      onSubmit={handleSubmit} 
      className={`${styles.form} ${className}`}
      noValidate
    >
      {fields.map(field => (
        <FormField
          key={field.name}
          {...field}
          value={values[field.name]}
          error={errors[field.name]}
          touched={touched[field.name]}
          onChange={handleChange}
          onBlur={handleBlur}
        />
      ))}
      
      {children}
      
      <div className={styles.formActions}>
        <button 
          type="submit" 
          disabled={isSubmitting}
          className={styles.submitButton}
        >
          {isSubmitting ? 'Отправка...' : submitText}
        </button>
        
        <button 
          type="button" 
          onClick={reset}
          className={styles.resetButton}
        >
          Сбросить
        </button>
      </div>
    </form>
  );
};

// Валидаторы
export const validators = {
  required: (value) => {
    if (!value || (typeof value === 'string' && value.trim() === '')) {
      return 'Это поле обязательно';
    }
    return null;
  },

  email: (value) => {
    if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      return 'Введите корректный email';
    }
    return null;
  },

  minLength: (min) => (value) => {
    if (value && value.length < min) {
      return `Минимум ${min} символов`;
    }
    return null;
  },

  maxLength: (max) => (value) => {
    if (value && value.length > max) {
      return `Максимум ${max} символов`;
    }
    return null;
  },

  number: (value) => {
    if (value && isNaN(value)) {
      return 'Введите число';
    }
    return null;
  },

  positiveNumber: (value) => {
    if (value && (isNaN(value) || Number(value) <= 0)) {
      return 'Введите положительное число';
    }
    return null;
  }
};

// Композитный валидатор
export const composeValidators = (...validators) => (value) => {
  for (const validator of validators) {
    const error = validator(value);
    if (error) return error;
  }
  return null;
};

export default EnhancedForm;
export { FormField }; 