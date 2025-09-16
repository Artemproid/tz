import React from 'react';
import ReferenceList from '../../components/reference-list';
import styles from './styles.module.css';

const SubcategoryList = () => {
  return (
    <div className={styles.container}>
      <ReferenceList
        title="Подкатегории"
        endpoint="/api/v1/my/subcategories/"
        fields={[
          {
            name: 'name',
            label: 'Название',
            type: 'text',
            required: true
          },
          {
            name: 'category',
            label: 'Категория',
            type: 'select',
            required: true
          }
        ]}
        dependencies={{
          category: '/api/v1/my/categories/'
        }}
      />
    </div>
  );
};

export default SubcategoryList; 