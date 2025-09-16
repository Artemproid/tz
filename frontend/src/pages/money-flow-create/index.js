import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import styles from './styles.module.css';
import api from '../../api';
import MetaTags from "react-meta-tags";

const MoneyFlowCreate = () => {
  const history = useHistory();
  const [formData, setFormData] = useState({
    created_at: new Date().toISOString().split('T')[0],
    status: '',
    type: '',
    category: '',
    subcategory: '',
    amount: '',
    comment: ''
  });

  const [statuses, setStatuses] = useState([]);
  const [types, setTypes] = useState([]);
  const [categories, setCategories] = useState([]);
  const [subcategories, setSubcategories] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Получаем данные справочников пользователя
        const statusesResponse = await api.getStatuses();
        const typesResponse = await api.getTypes();
        const categoriesResponse = await api.getCategories();
        const subcategoriesResponse = await api.getSubcategories();
        
        console.log('API responses:', { statusesResponse, typesResponse, categoriesResponse, subcategoriesResponse });

        // Извлекаем results из ответов API
        const statusesData = statusesResponse?.results || statusesResponse || [];
        const typesData = typesResponse?.results || typesResponse || [];
        const categoriesData = categoriesResponse?.results || categoriesResponse || [];
        const subcategoriesData = subcategoriesResponse?.results || subcategoriesResponse || [];

        console.log('Extracted data:', { statusesData, typesData, categoriesData, subcategoriesData });

        setStatuses(Array.isArray(statusesData) ? statusesData : []);
        setTypes(Array.isArray(typesData) ? typesData : []);
        setCategories(Array.isArray(categoriesData) ? categoriesData : []);
        setSubcategories(Array.isArray(subcategoriesData) ? subcategoriesData : []);
      } catch (err) {
        console.error('Ошибка при загрузке данных:', err);
        setError('Не удалось загрузить справочники');
      }
    };

    fetchData();
  }, []);

  const filteredSubcategories = subcategories.filter(
    sub => sub.category === Number(formData.category)
  );

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    if (name === 'category') {
      setFormData(prev => ({
        ...prev,
        subcategory: ''
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createMoneyFlow(formData);
      // Перенаправляем на главную страницу, где показывается список операций
      history.push('/');
    } catch (err) {
      setError('Не удалось создать запись');
      console.error('Ошибка создания записи:', err);
    }
  };

  return (
    <div className={styles.container}>
      <MetaTags>
        <title>Создание записи</title>
        <meta name="description" content="Создание денежной записи" />
        <meta property="og:title" content="Создание записи" />
      </MetaTags>
      <h1 className={styles.title}>Создание новой записи</h1>
      
      {error && <div className={styles.error}>{error}</div>}
      
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label>Дата:</label>
          <input
            type="date"
            name="created_at"
            value={formData.created_at}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label>Статус:</label>
          <select 
            name="status" 
            value={formData.status}
            onChange={handleChange}
            required
          >
            <option value="">Выберите статус</option>
            {statuses.map(status => (
              <option key={status.id} value={status.id}>
                {status.name}
              </option>
            ))}
          </select>
          {statuses.length === 0 && (
            <small className={styles.hint}>
              Сначала создайте статусы в разделе "Статусы"
            </small>
          )}
        </div>
        
        <div className={styles.formGroup}>
          <label>Тип:</label>
          <select 
            name="type" 
            value={formData.type}
            onChange={handleChange}
            required
          >
            <option value="">Выберите тип</option>
            {types.map(type => (
              <option key={type.id} value={type.id}>
                {type.name}
              </option>
            ))}
          </select>
          {types.length === 0 && (
            <small className={styles.hint}>
              Сначала создайте типы в разделе "Типы операций"
            </small>
          )}
        </div>

        <div className={styles.formGroup}>
          <label>Категория:</label>
          <select 
            name="category" 
            value={formData.category}
            onChange={handleChange}
            required
          >
            <option value="">Выберите категорию</option>
            {categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
          {categories.length === 0 && (
            <small className={styles.hint}>
              Сначала создайте категории в разделе "Категории"
            </small>
          )}
        </div>

        <div className={styles.formGroup}>
          <label>Подкатегория:</label>
          <select 
            name="subcategory" 
            value={formData.subcategory}
            onChange={handleChange}
            required
            disabled={!formData.category}
          >
            <option value="">Выберите подкатегорию</option>
            {filteredSubcategories.map(subcategory => (
              <option key={subcategory.id} value={subcategory.id}>
                {subcategory.name}
              </option>
            ))}
          </select>
          {formData.category && filteredSubcategories.length === 0 && (
            <small className={styles.hint}>
              Сначала создайте подкатегории для выбранной категории в разделе "Подкатегории"
            </small>
          )}
        </div>

        <div className={styles.formGroup}>
          <label>Сумма:</label>
          <input
            type="number"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            min="0"
            step="0.01"
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label>Комментарий:</label>
          <textarea
            name="comment"
            value={formData.comment}
            onChange={handleChange}
            rows="4"
          />
        </div>

        <div className={styles.buttons}>
          <button type="submit" className={styles.submitButton}>
            Создать запись
          </button>
          <button 
            type="button" 
            onClick={() => history.push('/')}
            className={styles.cancelButton}
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  );
};

export default MoneyFlowCreate;