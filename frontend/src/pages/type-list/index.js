import React from 'react';
import ReferenceList from '../../components/reference-list';

const TypeList = () => {
  return (
    <ReferenceList
      title="Типы операций"
      endpoint="/api/v1/my/types/"
      itemName="тип"
      fields={[
        {
          name: 'name',
          label: 'Название',
          type: 'text',
          required: true
        }
      ]}
    />
  );
};

export default TypeList; 