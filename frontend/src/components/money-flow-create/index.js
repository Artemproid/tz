const fetchSubcategories = async (categoryId) => {
  try {
    const response = await api.get(`/api/subcategories/?category=${categoryId}`);
    setSubcategories(response.data);
  } catch (error) {
    console.error('Error fetching subcategories:', error);
  }
}; 