import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import { useState, useEffect } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'
import MoneyFlowList from '../../components/money-flow-list'

const HomePage = () => {
  const [moneyFlows, setMoneyFlows] = useState([])
  const [filters, setFilters] = useState({})
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  const loadData = async (currentPage, currentFilters) => {
    try {
      const data = await api.getMoneyFlows(currentPage, currentFilters)
      setMoneyFlows(data.results)
      setTotalPages(Math.ceil(data.count / 10))
    } catch (err) {
      console.error('Ошибка при загрузке данных:', err)
    }
  }

  useEffect(() => {
    loadData(page, filters)
  }, [page, filters])

  const handleFilterChange = (newFilters) => {
    setPage(1)
    setFilters(newFilters)
  }

  const handlePageChange = (newPage) => {
    setPage(newPage)
  }

  return <Main>
    <Container>
      <MetaTags>
        <title>Учет финансов</title>
        <meta name="description" content="Система учета финансов" />
        <meta property="og:title" content="Учет финансов" />
      </MetaTags>
      <div className={styles.header}>
        <h1>Учет финансов</h1>
      </div>
      <MoneyFlowList 
        moneyFlows={moneyFlows}
        filters={filters}
        onFilterChange={handleFilterChange}
        page={page}
        totalPages={totalPages}
        onPageChange={handlePageChange}
      />
    </Container>
  </Main>
}

export default HomePage

