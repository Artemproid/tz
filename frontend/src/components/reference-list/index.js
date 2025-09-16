import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';
import api from '../../api';

const ReferenceList = ({ title, endpoint, fields = [{ name: 'name', label: 'Название', type: 'text', required: true }], dependencies = {}, columnHeaders = {} }) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editItem, setEditItem] = useState({});
  const [newItem, setNewItem] = useState({});
  const [dependencyData, setDependencyData] = useState({});

  // Определяем API методы на основе endpoint
  const getApiMethod = (action) => {
    if (endpoint.includes('/my/statuses/')) {
      return {
        get: api.getStatuses,
        create: api.createStatus,
        update: api.updateStatus,
        delete: api.deleteStatus
      }[action];
    }
    if (endpoint.includes('/my/types/')) {
      return {
        get: api.getTypes,
        create: api.createType,
        update: api.updateType,
        delete: api.deleteType
      }[action];
    }
    if (endpoint.includes('/my/categories/')) {
      return {
        get: api.getCategories,
        create: api.createCategory,
        update: api.updateCategory,
        delete: api.deleteCategory
      }[action];
    }
    if (endpoint.includes('/my/subcategories/')) {
      return {
        get: api.getSubcategories,
        create: api.createSubcategory,
        update: api.updateSubcategory,
        delete: api.deleteSubcategory
      }[action];
    }
    return null;
  };

  // Загрузка зависимостей
  useEffect(() => {
    const loadDependencies = async () => {
      const data = {};
      for (const [key, depEndpoint] of Object.entries(dependencies)) {
        try {
          let response;
          if (depEndpoint.includes('types')) {
            response = await api.getTypes();
          } else if (depEndpoint.includes('categories')) {
            response = await api.getCategories();
          }
          data[key] = response?.results || response || [];
        } catch (error) {
          console.error(`Error loading ${key}:`, error);
          data[key] = [];
        }
      }
      setDependencyData(data);
    };

    if (Object.keys(dependencies).length > 0) {
      loadDependencies();
    }
  }, [dependencies]);

  const fetchItems = async () => {
    try {
      setLoading(true);
      setError(null);
      const apiMethod = getApiMethod('get');
      if (!apiMethod) {
        throw new Error('API method not found');
      }
      const response = await apiMethod();
      const data = response?.results || response || [];
      const sortedData = Array.isArray(data) ? data.sort((a, b) => a.id - b.id) : [];
      setItems(sortedData);
    } catch (err) {
      setError('Ошибка при загрузке данных');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, [endpoint]);

  const handleInputChange = (fieldName, value) => {
    setNewItem(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  const handleCreate = async () => {
    const requiredFields = fields.filter(f => f.required);
    if (!requiredFields.every(field => newItem[field.name])) {
      setError('Заполните все обязательные поля');
      return;
    }
    
    try {
      const apiMethod = getApiMethod('create');
      if (!apiMethod) {
        throw new Error('Create API method not found');
      }
      await apiMethod(newItem);
      setNewItem({});
      setIsCreating(false);
      setError(null);
      // Обновляем список после создания
      await fetchItems();
    } catch (error) {
      console.error('Error creating item:', error);
      setError('Ошибка при создании элемента');
    }
  };

  const handleCancel = () => {
    setIsCreating(false);
    setNewItem({});
    setError(null);
  };

  const handleEdit = (item) => {
    setEditingId(item.id);
    setEditItem(item);
  };

  const handleUpdate = async () => {
    try {
      const apiMethod = getApiMethod('update');
      if (!apiMethod) {
        throw new Error('Update API method not found');
      }
      await apiMethod({ id: editingId, ...editItem });
      setEditingId(null);
      setError(null);
      // Обновляем список после обновления
      await fetchItems();
    } catch (error) {
      console.error('Error updating item:', error);
      setError('Ошибка при обновлении');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Вы уверены, что хотите удалить эту запись?')) {
      try {
        const apiMethod = getApiMethod('delete');
        if (!apiMethod) {
          throw new Error('Delete API method not found');
        }
        await apiMethod({ id });
        setError(null);
        // Обновляем список после удаления
        await fetchItems();
      } catch (error) {
        console.error('Error deleting item:', error);
        setError('Ошибка при удалении');
      }
    }
  };

  const handleEditInputChange = (fieldName, value) => {
    setEditItem(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  const renderFieldValue = (field, item) => {
    const fieldName = field.name;
    if (dependencies[fieldName]) {
      const dependencyValue = dependencyData[fieldName]?.find(
        dep => dep.id === (typeof item[fieldName] === 'string' ? parseInt(item[fieldName]) : item[fieldName])
      );
      return dependencyValue?.name || `Не указан(а)`;
    }
    return item[fieldName];
  };

  const renderInput = (field, value, onChange, isEdit = false) => {
    const { name, type, required } = field;
    
    if (dependencies[name]) {
      return (
        <select
          key={name}
          value={value || ''}
          onChange={(e) => onChange(name, e.target.value)}
          className={styles.select}
          required={required}
        >
          <option value="">Выберите {field.label}</option>
          {dependencyData[name]?.map(dep => (
            <option key={dep.id} value={dep.id}>
              {dep.name}
            </option>
          ))}
        </select>
      );
    }

    switch (type) {
      case 'textarea':
        return (
          <textarea
            key={name}
            value={value || ''}
            onChange={(e) => onChange(name, e.target.value)}
            placeholder={`Введите ${field.label.toLowerCase()}`}
            className={styles.textarea}
            required={required}
          />
        );
      default:
        return (
          <input
            key={name}
            type={type}
            value={value || ''}
            onChange={(e) => onChange(name, e.target.value)}
            placeholder={`Введите ${field.label.toLowerCase()}`}
            className={styles.input}
            required={required}
          />
        );
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>{title}</h2>
        <button 
          className={styles.createButton}
          onClick={() => setIsCreating(true)}
        >
          Создать
        </button>
      </div>
      
      {error && <div className={styles.error}>{error}</div>}
      
      <div className={styles.list}>
        <div className={styles.headerRow}>
          {fields.map(field => (
            <span key={field.name} className={styles.headerCell}>
              {field.label}
            </span>
          ))}
          <span className={styles.headerCell}>Действия</span>
        </div>

        {isCreating && (
          <div className={styles.newItem}>
            {fields.map(field => renderInput(field, newItem[field.name], handleInputChange))}
            <div className={styles.actions}>
              <button 
                className={styles.actionButton}
                onClick={handleCreate}
              >
                ✓
              </button>
              <button 
                className={styles.actionButton}
                onClick={handleCancel}
              >
                ✕
              </button>
            </div>
          </div>
        )}
        
        {loading ? (
          <div className={styles.loading}>Загрузка...</div>
        ) : items.length > 0 ? (
          items.map(item => (
            <div key={item.id} className={styles.item}>
              {editingId === item.id ? (
                <>
                  {fields.map(field => renderInput(field, editItem[field.name], handleEditInputChange, true))}
                  <div className={styles.actions}>
                    <button className={styles.actionButton} onClick={handleUpdate}>✓</button>
                    <button className={styles.actionButton} onClick={() => setEditingId(null)}>✕</button>
                  </div>
                </>
              ) : (
                <>
                  <div className={styles.itemFields}>
                    {fields.map(field => (
                      <span key={field.name} className={styles.itemField}>
                        {renderFieldValue(field, item)}
                      </span>
                    ))}
                  </div>
                  <div className={styles.actions}>
                    <button className={styles.actionButton} onClick={() => handleEdit(item)}>✎</button>
                    <button className={styles.actionButton} onClick={() => handleDelete(item.id)}>🗑</button>
                  </div>
                </>
              )}
            </div>
          ))
        ) : (
          <div className={styles.emptyMessage}>
            Нет данных
          </div>
        )}
      </div>
    </div>
  );
};

export default ReferenceList; 