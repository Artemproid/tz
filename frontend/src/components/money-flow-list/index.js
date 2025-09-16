import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import styles from './styles.module.css';
import api from '../../api';

const MoneyFlowList = ({ 
  moneyFlows = [], 
  filters,
  onFilterChange,
  page,
  totalPages,
  onPageChange
}) => {
  const history = useHistory();
  const [debounceTimer, setDebounceTimer] = useState(null);
  const [dateRange, setDateRange] = useState({
    startDate: '',
    endDate: ''
  });

  const handleRowClick = (id) => {
    history.push(`/money-flow/${id}`);
  };

  const handleFilterChange = (name, value) => {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    setDebounceTimer(
      setTimeout(() => {
        onFilterChange({ ...filters, [name]: value });
      }, 100)
    );
  };

  const handleDateChange = (e) => {
    const { name, value } = e.target;
    setDateRange(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const getFilteredData = async () => {
    try {
      const params = new URLSearchParams(filters);
      if (dateRange.startDate) params.append('start_date', dateRange.startDate);
      if (dateRange.endDate) params.append('end_date', dateRange.endDate);
      
      onFilterChange(Object.fromEntries(params));
    } catch (error) {
      console.error('Error applying filters:', error);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.filters}>
        <div className={styles.dateRange}>
          <input
            type="date"
            name="startDate"
            value={dateRange.startDate}
            onChange={handleDateChange}
            className={styles.dateInput}
          />
          <span>—</span>
          <input
            type="date"
            name="endDate"
            value={dateRange.endDate}
            onChange={handleDateChange}
            className={styles.dateInput}
          />
          <button 
            className={styles.filterButton}
            onClick={getFilteredData}
          >
            Применить
          </button>
        </div>
        <input
          type="text"
          className={styles.filter}
          placeholder="Статус"
          value={filters.status || ''}
          onChange={(e) => handleFilterChange('status', e.target.value)}
        />
        <input
          type="text"
          className={styles.filter}
          placeholder="Тип"
          value={filters.type || ''}
          onChange={(e) => handleFilterChange('type', e.target.value)}
        />
        <input
          type="text"
          className={styles.filter}
          placeholder="Категория"
          value={filters.category || ''}
          onChange={(e) => handleFilterChange('category', e.target.value)}
        />
        <input
          type="text"
          className={styles.filter}
          placeholder="Подкатегория"
          value={filters.subcategory || ''}
          onChange={(e) => handleFilterChange('subcategory', e.target.value)}
        />
      </div>

      <div className={styles.table}>
        <div className={styles.header}>
          <div className={styles.cell}>Дата</div>
          <div className={styles.cell}>Статус</div>
          <div className={styles.cell}>Тип</div>
          <div className={styles.cell}>Категория</div>
          <div className={styles.cell}>Подкатегория</div>
          <div className={styles.cell}>Сумма</div>
          <div className={styles.cell}>Комментарий</div>
        </div>
        {moneyFlows.map(flow => (
          <div 
            key={flow.id} 
            className={styles.row}
            onClick={() => handleRowClick(flow.id)}
          >
            <div className={styles.cell}>{new Date(flow.created_at).toLocaleDateString()}</div>
            <div className={styles.cell}>{flow.status.name}</div>
            <div className={styles.cell}>{flow.type.name}</div>
            <div className={styles.cell}>{flow.category.name}</div>
            <div className={styles.cell}>{flow.subcategory.name}</div>
            <div className={`${styles.cell} ${flow.type.name === 'Доход' ? styles.income : styles.expense}`}>
              {flow.amount} ₽
            </div>
            <div className={styles.cell}>{flow.comment}</div>
          </div>
        ))}
      </div>

      <div className={styles.pagination}>
        <button
          className={styles.pageButton}
          disabled={page === 1}
          onClick={() => onPageChange(page - 1)}
        >
          Назад
        </button>
        <span className={styles.pageInfo}>
          Страница {page} из {totalPages}
        </span>
        <button
          className={styles.pageButton}
          disabled={page === totalPages}
          onClick={() => onPageChange(page + 1)}
        >
          Вперед
        </button>
      </div>
    </div>
  );
};

export default MoneyFlowList;   