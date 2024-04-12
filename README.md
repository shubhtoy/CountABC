
![Logo](https://countabc.xyz/static/img/logo.png)

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/33991252-bd6b3ddf-3797-4e7b-a0c0-7a4472050606?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D33991252-bd6b3ddf-3797-4e7b-a0c0-7a4472050606%26entityType%3Dcollection%26workspaceId%3Df1151ef8-870c-427d-bc4a-1d914c7e8e59)

[Postman Documentation]("https://documenter.getpostman.com/view/33991252/2sA35MxJR8")
# **CountABC.xyz API Documentation**

This markdown document serves as comprehensive documentation for the CountABC.xyz API, a service designed to facilitate the creation and management of simple numeric counters, effectively serving as an Integer as a Service (IaaS). Through this API, users can efficiently track various events and counts in their applications.

## **Overview**

The CountABC.xyz API facilitates the creation of numeric counters, enabling users to monitor events and counts in their applications. It provides functionalities for creating, resetting, incrementing, and decrementing counters.

## **Features**

- Create and manage numeric counters.
- Reset counter values when necessary.
- Increment or decrement counters as required.
- Track various events efficiently.

## **Tech Stack**

- **Endpoints**: Base API path: `https://api.countabc.xyz`
- **Data Format**: JSON
- **Cross-Origin Resource Sharing (CORS)**: Supported
- **SSL**: Supported

## **Endpoints**

### **Create Counter**
- **Endpoint**: `/create`
- **Description**: Creates a new counter.
- **Example**: `POST /create`

### **Reset Counter**
- **Endpoint**: `/set/:namespace?/:key?value=:value`
- **Description**: Resets the value of a counter.
- **Example**: `POST /set/test_namespace/test_key?value=0`

### **Increment/Decrement Counter**
- **Endpoint**: `/update/:namespace?/:key?amount=:amount`
- **Description**: Updates a counter by a specified amount.
- **Example**: `POST /update/test_namespace/test_key?amount=5`

### **Track Events**
- **Endpoint**: `/hit/:namespace?/:key`
- **Description**: Increments a counter by one.
- **Example**: `POST /hit/test_namespace/test_key`

### **Get Counter Value**
- **Endpoint**: `/get/:namespace?/:key`
- **Description**: Retrieves the value of a counter.
- **Example**: `GET /get/test_namespace/test_key`

### **Get Counter Information**
- **Endpoint**: `/info/:namespace?/:key`
- **Description**: Retrieves information about a counter.
- **Example**: `GET /info/test_namespace/test_key`

### **Get Statistics**
- **Endpoint**: `/stats`
- **Description**: Retrieves statistics about CountABC.
- **Example**: `GET /stats`

### **Additional Endpoints**

#### **Delete Counter**
- **Endpoint**: `/delete/:namespace?/:key`
- **Description**: Deletes a counter.
- **Example**: `DELETE /delete/test_namespace/test_key`

#### **Expire Counter**
- **Endpoint**: `/expire/:namespace?/:key?expiration=:expiration`
- **Description**: Sets an expiration time for a counter.
- **Example**: `POST /expire/test_namespace/test_key?expiration=3600`

## **Usage**

Users can utilize the endpoints provided by the CountABC.xyz API to create, manage, and track numeric counters in their applications.

## **FAQ**

- **Is the API documentation available?**: Yes, you're reading it now.
- **Is the API free?**: Yes, it's completely free.
- **Rate Limiting?**: Key retrieval and updating have no limits. Key creation is limited to 20/IP/s.
- **Can I delete a counter?**: Yes, you can delete a counter using the `/delete` endpoint.

## **Contact and Issues**

For any issues, suggestions, or inquiries, users can contact the CountABC.xyz team via email at [your_email@example.com](mailto:your_email@example.com).











