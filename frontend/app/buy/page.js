// pages/index.js
'use client';
import React, { useState } from 'react';
import axios from 'axios';


const Buy = () => {
  const [itemId, setItemId] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');

  const handleBuyItem = async (event) => {
    event.preventDefault(); // 阻止表单的默认提交行为

    try {
      const result = await axios.post('http://localhost:8000/buy', {
        item_id: itemId,
        quantity: parseInt(quantity, 10)
      });
      setResponse(`Purchase successful! Remaining stock: ${result.data.remaining_stock}`);
      setError('');
    } catch (err) {
      if (err.response) {
        // 处理来自后端的错误响应
        setError(`Error: ${err.response.status} - ${err.response.data.detail}`);
      } else {
        setError('Error: Network Error or Server is not responding');
      }
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Buy Item</h1>
      <form onSubmit={handleBuyItem}>
        <div>
          <label htmlFor="itemId">Item ID:</label>
          <input
            id="itemId"
            type="text"
            value={itemId}
            onChange={(e) => setItemId(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="quantity">Quantity:</label>
          <input
            id="quantity"
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            min="1"
            required
          />
        </div>
        <button type="submit">Buy</button>
      </form>
      {response && <p>{response}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default Buy;
