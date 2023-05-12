
  function deleteCustomer(rowId) {
    fetch("/delete-customer", {
      method: "POST",
      body: JSON.stringify({ rowId: rowId }),
    }).then((_res) => {
      window.location.href = "/customer";
    });
  }


  function deleteProduct(rowId) {
    fetch("/delete-product", {
      method: "POST",
      body: JSON.stringify({ rowId: rowId }),
    }).then((_res) => {
      window.location.href = "/product_list";
    });
  }

  function deleteOrderItem(orderItemID,orderID) {
    fetch("/delete-orderItem", {
      method: "POST",
      body: JSON.stringify({ orderItemID: orderItemID }),
    }).then((_res) => {
      window.location.href = "/new_order/"+ orderID;
    });
  }


  