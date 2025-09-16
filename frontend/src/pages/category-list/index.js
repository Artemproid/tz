import React from 'react';
import ReferenceList from '../../components/reference-list';
import styles from './styles.module.css';

const CategoryList = () => {
  return (
    <div className={styles.container}>
      <ReferenceList
        title="Категории"
        endpoint="/api/v1/my/categories/"
        fields={[
          {
            name: 'name',
            label: 'Название',
            type: 'text',
            required: true
          },
          {
            name: 'type',
            label: 'Тип операции',
            type: 'select',
            required: true
          }
        ]}
        dependencies={{
          type: '/api/v1/my/types/'
        }}
      />
    </div>
  );
};

export default CategoryList; 