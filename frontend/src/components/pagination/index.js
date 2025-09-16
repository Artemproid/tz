import styles from './styles.module.css'
import cn from 'classnames'

const Pagination = ({ count, limit = 6, page = 1, onPageChange }) => {
  const totalPages = Math.ceil(count / limit)

  return <div className={styles.pagination}>
    <button
      className={cn(styles.button, {
        [styles.button_disabled]: page === 1
      })}
      disabled={page === 1}
      onClick={() => onPageChange(page - 1)}
    >
      Назад
    </button>
    <button
      className={cn(styles.button, {
        [styles.button_disabled]: page === totalPages
      })}
      disabled={page === totalPages}
      onClick={() => onPageChange(page + 1)}
    >
      Вперед
    </button>
  </div>
}

export default Pagination
