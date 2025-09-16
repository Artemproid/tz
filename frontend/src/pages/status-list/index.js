import React from 'react';
import ReferenceList from '../../components/reference-list';

const StatusList = () => {
  return (
    <ReferenceList
      title="Статусы"
      endpoint="/api/v1/my/statuses/"
      itemName="статус"
      fields={[
        {
          name: 'name',
          label: 'Название',
          type: 'text',
          required: true
        },
        {
          name: 'description',
          label: 'Описание',
          type: 'textarea',
          required: false
        }
      ]}
    />
  );
};

export default StatusList; 