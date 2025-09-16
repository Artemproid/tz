import React, { useEffect, useState } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import api from '../../api';
import styles from './styles.module.css';

const MoneyFlowDetail = () => {
  const { id } = useParams();
  const history = useHistory();
  const [moneyFlow, setMoneyFlow] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.getMoneyFlow(id)
      .then(data => {
        setMoneyFlow(data);
      })
      .catch(err => {
        console.error('Ошибка при загрузке записи:', err);
        setError('Не удалось загрузить запись');
      });
  }, [id]);

  const handleDelete = async () => {
    if (window.confirm('Вы уверены, что хотите удалить эту запись?')) {
      try {
        await api.deleteItem('/api/money-flows/', id);
        history.push('/'); // Возвращаемся на главную после удаления
      } catch (err) {
        console.error('Ошибка при удалении:', err);
        setError('Не удалось удалить запись');
      }
    }
  };

  if (error) return <div className={styles.error}>{error}</div>;
  if (!moneyFlow) return <div>Загрузка...</div>;

  return (
    <div className={styles.container}>
      <h2>Детали записи</h2>
      <div className={styles.details}>
        <div className={styles.row}>
          <span className={styles.label}>Дата:</span>
          <span className={styles.value}>
            {new Date(moneyFlow.created_at).toLocaleDateString()}
          </span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Статус:</span>
          <span className={styles.value}>{moneyFlow.status.name}</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Тип:</span>
          <span className={styles.value}>{moneyFlow.type.name}</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Категория:</span>
          <span className={styles.value}>{moneyFlow.category.name}</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Подкатегория:</span>
          <span className={styles.value}>{moneyFlow.subcategory.name}</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Сумма:</span>
          <span className={`${styles.value} ${moneyFlow.type.name === 'Доход' ? styles.income : styles.expense}`}>
            {moneyFlow.amount} ₽
          </span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Комментарий:</span>
          <span className={styles.value}>{moneyFlow.comment}</span>
        </div>
      </div>
      <div className={styles.buttons}>
        <button 
          className={`${styles.button} ${styles.edit}`}
          onClick={() => history.push(`/money-flow/${id}/edit`)}
        >
          Редактировать
        </button>
        <button 
          className={`${styles.button} ${styles.delete}`}
          onClick={handleDelete}
        >
          Удалить
        </button>
        <button 
          className={styles.button}
          onClick={() => history.push('/')}
        >
          Назад к списку
        </button>
      </div>
    </div>
  );
};

export default MoneyFlowDetail;