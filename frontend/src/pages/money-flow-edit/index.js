import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import api from '../../api';
import styles from './styles.module.css';

const MoneyFlowEdit = () => {
  const { id } = useParams();
  const history = useHistory();
  const [formData, setFormData] = useState({
    created_at: '',
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
    // Загружаем данные записи
    api.getMoneyFlow(id)
      .then(data => {
        setFormData({
          created_at: data.created_at,
          status: data.status.id,
          type: data.type.id,
          category: data.category.id,
          subcategory: data.subcategory.id,
          amount: data.amount,
          comment: data.comment
        });
      })
      .catch(err => {
        console.error('Ошибка при загрузке записи:', err);
        setError('Не удалось загрузить запись');
      });

    // Загружаем справочники
    api.getItems('/api/statuses/').then(data => setStatuses(data));
    api.getItems('/api/types/').then(data => setTypes(data));
    api.getItems('/api/categories/').then(data => setCategories(data));
    api.getItems('/api/subcategories/').then(data => setSubcategories(data));
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.updateItem('/api/money-flows/', id, formData);
      history.push(`/money-flow/${id}`);
    } catch (err) {
      console.error('Ошибка при обновлении:', err);
      setError('Не удалось обновить запись');
    }
  };

  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.container}>
      <h2>Редактирование записи</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label>Дата:</label>
          <input
            type="date"
            name="created_at"
            value={formData.created_at}
            onChange={handleChange}
          />
        </div>

        <div className={styles.formGroup}>
          <label>Статус:</label>
          <select name="status" value={formData.status} onChange={handleChange}>
            {statuses.map(status => (
              <option key={status.id} value={status.id}>{status.name}</option>
            ))}
          </select>
        </div>

        <div className={styles.formGroup}>
          <label>Тип:</label>
          <select name="type" value={formData.type} onChange={handleChange}>
            {types.map(type => (
              <option key={type.id} value={type.id}>{type.name}</option>
            ))}
          </select>
        </div>

        <div className={styles.formGroup}>
          <label>Категория:</label>
          <select name="category" value={formData.category} onChange={handleChange}>
            {categories.map(category => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
        </div>

        <div className={styles.formGroup}>
          <label>Подкатегория:</label>
          <select name="subcategory" value={formData.subcategory} onChange={handleChange}>
            {subcategories
              .filter(sub => sub.category === formData.category)
              .map(subcategory => (
                <option key={subcategory.id} value={subcategory.id}>
                  {subcategory.name}
                </option>
              ))}
          </select>
        </div>

        <div className={styles.formGroup}>
          <label>Сумма:</label>
          <input
            type="number"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
          />
        </div>

        <div className={styles.formGroup}>
          <label>Комментарий:</label>
          <textarea
            name="comment"
            value={formData.comment}
            onChange={handleChange}
            rows={4}
          />
        </div>

        <div className={styles.buttons}>
          <button type="submit" className={`${styles.button} ${styles.save}`}>
            Сохранить
          </button>
          <button
            type="button"
            className={styles.button}
            onClick={() => history.push(`/money-flow/${id}`)}
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  );
};

export default MoneyFlowEdit; 