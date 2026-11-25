# Sample Interview Questions Dataset
# Used as fallback when LLM generation is not available or slow

SAMPLE_QUESTIONS = {
    "frontend_developer": {
        "junior": [
            {
                "question": "Explain the difference between let, const, and var in JavaScript.",
                "ideal_answer": "var is function-scoped and hoisted, let and const are block-scoped. const creates an immutable binding, while let allows reassignment. Modern JavaScript prefers const and let over var.",
                "key_points": ["Scope (function vs block)", "Hoisting", "Mutability", "Best practices"],
                "evaluation_criteria": ["Understands scoping", "Knows hoisting behavior", "Can recommend best practices"]
            },
            {
                "question": "What is the CSS Box Model?",
                "ideal_answer": "The box model is a fundamental concept in CSS. It consists of content, padding, border, and margin. Content is the inner area, padding is inside the border, border surrounds the padding, and margin is outside the border.",
                "key_points": ["Content", "Padding", "Border", "Margin", "box-sizing property"],
                "evaluation_criteria": ["Can explain each component", "Understands impact on layout"]
            },
            {
                "question": "How does event delegation work in JavaScript?",
                "ideal_answer": "Event delegation uses event bubbling to handle events on parent elements instead of individual children. This improves performance and allows handling events for dynamically added elements.",
                "key_points": ["Event bubbling", "Performance benefits", "Dynamic element handling"],
                "evaluation_criteria": ["Understands the concept", "Can explain benefits"]
            }
        ],
        "mid": [
            {
                "question": "Explain React Hooks and why they were introduced.",
                "ideal_answer": "Hooks allow you to use state and other React features without writing class components. They were introduced to make code more reusable and easier to understand. useState, useEffect, useContext are commonly used hooks.",
                "key_points": ["State management", "Lifecycle in functional components", "Reusability", "Rules of hooks"],
                "evaluation_criteria": ["Understands purpose", "Can name common hooks"]
            },
            {
                "question": "What is the virtual DOM and how does React use it?",
                "ideal_answer": "The virtual DOM is an in-memory representation of the real DOM. React uses it to compare changes and efficiently update only the parts of the real DOM that changed, improving performance.",
                "key_points": ["Virtual vs Real DOM", "Reconciliation", "Performance optimization"],
                "evaluation_criteria": ["Understands the concept", "Can explain the benefit"]
            }
        ],
        "senior": [
            {
                "question": "How would you optimize the performance of a large React application?",
                "ideal_answer": "Consider: code splitting and lazy loading, memoization of expensive computations, efficient state management, avoiding unnecessary re-renders, server-side rendering, and monitoring with performance tools.",
                "key_points": ["Code splitting", "Memoization", "State management", "Rendering optimization"],
                "evaluation_criteria": ["Holistic thinking", "Multiple approaches", "Practical experience"]
            }
        ]
    },
    "backend_developer": {
        "junior": [
            {
                "question": "Explain the HTTP request/response cycle.",
                "ideal_answer": "Client sends HTTP request to server with method, headers, and body. Server processes and sends back response with status code, headers, and body. Common methods: GET, POST, PUT, DELETE.",
                "key_points": ["HTTP methods", "Status codes", "Headers", "Request/response structure"],
                "evaluation_criteria": ["Understands basic flow", "Knows common methods"]
            },
            {
                "question": "What is a RESTful API?",
                "ideal_answer": "REST (Representational State Transfer) uses HTTP methods to perform operations on resources identified by URLs. Get retrieves, POST creates, PUT updates, DELETE removes. Responses are typically JSON.",
                "key_points": ["HTTP methods", "Resource-based URLs", "Stateless", "JSON responses"],
                "evaluation_criteria": ["Understands principles", "Can design endpoints"]
            }
        ],
        "mid": [
            {
                "question": "Explain database normalization and its forms (1NF, 2NF, 3NF).",
                "ideal_answer": "Normalization organizes data to minimize redundancy and dependency anomalies. 1NF removes repeating groups, 2NF ensures all fields depend on the primary key, 3NF ensures no transitive dependencies.",
                "key_points": ["Normal forms", "Reduces redundancy", "Improves integrity", "Trade-offs"],
                "evaluation_criteria": ["Understands normal forms", "Can apply in practice"]
            },
            {
                "question": "Describe the CAP theorem and its implications.",
                "ideal_answer": "Distributed systems can guarantee at most two of: Consistency, Availability, Partition tolerance. You must choose which two to prioritize based on your use case.",
                "key_points": ["Consistency", "Availability", "Partition tolerance", "Trade-offs"],
                "evaluation_criteria": ["Understands the theorem", "Can give examples"]
            }
        ]
    },
    "data_analyst": {
        "junior": [
            {
                "question": "Write a SQL query to find the top 5 customers by total purchases.",
                "ideal_answer": "SELECT customer_id, SUM(amount) as total_purchases FROM orders GROUP BY customer_id ORDER BY total_purchases DESC LIMIT 5;",
                "key_points": ["SELECT, FROM, GROUP BY", "Aggregation functions", "ORDER BY, LIMIT"],
                "evaluation_criteria": ["Correct syntax", "Logical approach"]
            },
            {
                "question": "Explain what a pivot table does.",
                "ideal_answer": "A pivot table reorganizes and summarizes data from a larger dataset. It groups data by one or more fields and calculates aggregate values (sum, count, average) for analysis.",
                "key_points": ["Data reorganization", "Aggregation", "Dimensional analysis"],
                "evaluation_criteria": ["Understands purpose", "Can use in Excel/BI tools"]
            }
        ],
        "mid": [
            {
                "question": "What is a JOIN in SQL? Explain INNER, LEFT, and RIGHT joins.",
                "ideal_answer": "JOINs combine rows from two tables based on related columns. INNER returns matching rows, LEFT returns all from left table plus matches, RIGHT returns all from right plus matches.",
                "key_points": ["INNER JOIN", "LEFT/RIGHT JOIN", "FULL OUTER JOIN", "Join conditions"],
                "evaluation_criteria": ["Understands join types", "Can write complex queries"]
            },
            {
                "question": "How do you handle missing data in analysis?",
                "ideal_answer": "Options include: remove rows/columns, impute with mean/median/mode, use forward/backward fill for time series, or document assumptions. Choice depends on data and context.",
                "key_points": ["Missing data strategies", "Statistical methods", "Documentation"],
                "evaluation_criteria": ["Considers context", "Knows multiple approaches"]
            }
        ]
    },
    "data_scientist": {
        "junior": [
            {
                "question": "Explain the difference between supervised and unsupervised learning.",
                "ideal_answer": "Supervised learning uses labeled data to train models (classification, regression). Unsupervised learning finds patterns in unlabeled data (clustering, dimensionality reduction).",
                "key_points": ["Training data", "Labels", "Model types", "Use cases"],
                "evaluation_criteria": ["Clear distinction", "Examples of each"]
            },
            {
                "question": "What is overfitting and how do you prevent it?",
                "ideal_answer": "Overfitting occurs when a model learns the training data too well and fails on new data. Prevention: use cross-validation, regularization, simplify the model, or get more training data.",
                "key_points": ["Overfitting vs underfitting", "Regularization", "Cross-validation", "Model complexity"],
                "evaluation_criteria": ["Understands the problem", "Knows solutions"]
            }
        ],
        "senior": [
            {
                "question": "Walk through your approach to building a machine learning model from scratch.",
                "ideal_answer": "1. Problem definition and data collection, 2. Exploratory data analysis, 3. Feature engineering, 4. Model selection and training, 5. Evaluation with appropriate metrics, 6. Hyperparameter tuning, 7. Deployment and monitoring.",
                "key_points": ["Systematic approach", "EDA importance", "Feature engineering", "Evaluation"],
                "evaluation_criteria": ["End-to-end thinking", "Practical experience"]
            }
        ]
    }
}

STUDY_TOPICS = {
    "frontend_developer": {
        "beginner": [
            {
                "topic": "HTML Fundamentals",
                "description": "Learn the structure of HTML, semantic elements, forms, and accessibility basics.",
                "importance": "Foundation for all web development",
                "key_points": ["HTML structure", "Semantic elements", "Forms and inputs", "Accessibility (a11y)"],
                "resources": ["MDN HTML Guide", "HTML.com", "W3C Standards"]
            },
            {
                "topic": "CSS Basics",
                "description": "Styling with CSS selectors, box model, flexbox, grid, and responsive design.",
                "importance": "Essential for styling and creating layouts",
                "key_points": ["Selectors and specificity", "Box model", "Flexbox", "CSS Grid", "Media queries"],
                "resources": ["CSS-Tricks", "MDN CSS Reference", "Can I Use"]
            },
            {
                "topic": "JavaScript Fundamentals",
                "description": "Variables, data types, functions, objects, arrays, ES6+ features, and async programming.",
                "importance": "Core language for frontend development",
                "key_points": ["Variables (var/let/const)", "Functions", "Objects and arrays", "ES6 features", "Async/await"],
                "resources": ["JavaScript.info", "MDN JavaScript", "Eloquent JavaScript"]
            }
        ],
        "intermediate": [
            {
                "topic": "React Fundamentals",
                "description": "Components, JSX, props, state, hooks, lifecycle, and component patterns.",
                "importance": "Most popular JavaScript framework",
                "key_points": ["Functional components", "Hooks", "State management", "Props", "Side effects"],
                "resources": ["Official React Docs", "React Documentation", "React Patterns"]
            },
            {
                "topic": "API Integration",
                "description": "Fetch API, axios, handling responses, error handling, and CORS.",
                "importance": "Critical for connecting frontend to backend",
                "key_points": ["Fetch API", "axios", "Error handling", "CORS", "Request/response"],
                "resources": ["MDN Fetch API", "API Design Guide", "REST principles"]
            }
        ],
        "advanced": [
            {
                "topic": "Performance Optimization",
                "description": "Code splitting, lazy loading, caching, bundle optimization, and monitoring.",
                "importance": "Build production-ready, high-performance applications",
                "key_points": ["Code splitting", "Lazy loading", "Caching strategies", "Bundle optimization"],
                "resources": ["Web Vitals", "Lighthouse", "Performance best practices"]
            },
            {
                "topic": "State Management",
                "description": "Redux, Context API, Zustand, or other state management solutions.",
                "importance": "Manage complex application state efficiently",
                "key_points": ["Redux", "Context API", "Actions and reducers", "Selectors"],
                "resources": ["Redux documentation", "React Context", "State management comparison"]
            }
        ]
    },
    "backend_developer": {
        "beginner": [
            {
                "topic": "Server Fundamentals",
                "description": "HTTP protocol, REST APIs, client-server architecture, and basic networking.",
                "importance": "Foundation of backend development",
                "key_points": ["HTTP methods", "REST principles", "Status codes", "Headers"],
                "resources": ["HTTP MDN", "REST guide", "Networking basics"]
            },
            {
                "topic": "Database Basics",
                "description": "Relational databases, SQL basics, CRUD operations, and schema design.",
                "importance": "Data storage and persistence",
                "key_points": ["SQL", "Schemas", "CRUD operations", "Relationships"],
                "resources": ["SQL Tutorial", "Database Design", "SQL recipes"]
            }
        ],
        "intermediate": [
            {
                "topic": "API Design",
                "description": "RESTful API design patterns, versioning, authentication, and rate limiting.",
                "importance": "Design scalable and maintainable APIs",
                "key_points": ["Resource design", "HTTP methods", "Error handling", "Documentation"],
                "resources": ["API Design Guide", "OpenAPI", "Authentication"]
            },
            {
                "topic": "Database Optimization",
                "description": "Indexing, query optimization, normalization, and performance tuning.",
                "importance": "Handle large datasets efficiently",
                "key_points": ["Indexing strategies", "Query optimization", "Normalization", "Caching"],
                "resources": ["Database tuning", "Query optimization", "Index strategies"]
            }
        ],
        "advanced": [
            {
                "topic": "System Design",
                "description": "Scalability, load balancing, microservices, caching, and distributed systems.",
                "importance": "Design systems that handle scale and high availability",
                "key_points": ["Architecture patterns", "Load balancing", "Microservices", "Caching"],
                "resources": ["System Design Primer", "Distributed systems", "Architecture patterns"]
            }
        ]
    },
    "data_analyst": {
        "beginner": [
            {
                "topic": "SQL Fundamentals",
                "description": "SELECT, WHERE, JOIN, GROUP BY, ORDER BY, and aggregation functions.",
                "importance": "Essential skill for querying databases",
                "key_points": ["SELECT queries", "Filtering", "Joins", "Aggregations"],
                "resources": ["SQL Tutorial", "LeetCode Database", "Mode Analytics SQL"]
            },
            {
                "topic": "Data Cleaning",
                "description": "Handling missing data, outliers, duplicates, and data quality issues.",
                "importance": "80% of data work is preparation",
                "key_points": ["Missing data", "Outliers", "Duplicates", "Data validation"],
                "resources": ["Data Cleaning guide", "Pandas documentation", "Tidy data"]
            }
        ],
        "intermediate": [
            {
                "topic": "Data Visualization",
                "description": "Creating effective visualizations with Tableau, Power BI, or Python.",
                "importance": "Communicate insights effectively",
                "key_points": ["Chart types", "Visual best practices", "Dashboard design"],
                "resources": ["Tableau public", "Power BI docs", "Data visualization guide"]
            },
            {
                "topic": "Statistical Analysis",
                "description": "Hypothesis testing, distributions, and exploratory data analysis.",
                "importance": "Foundation for analytical insights",
                "key_points": ["Distributions", "Hypothesis testing", "Correlation", "Regression"],
                "resources": ["Statistics guide", "Khan Academy", "A/B testing"]
            }
        ],
        "advanced": [
            {
                "topic": "Advanced Analytics",
                "description": "Time series analysis, forecasting, segmentation, and predictive modeling.",
                "importance": "Drive business impact with advanced techniques",
                "key_points": ["Time series", "Forecasting", "Clustering", "Prediction"],
                "resources": ["Time series guide", "Forecasting methods", "Analytics guide"]
            }
        ]
    },
    "data_scientist": {
        "beginner": [
            {
                "topic": "Python Fundamentals",
                "description": "Python basics, libraries (NumPy, Pandas), and data manipulation.",
                "importance": "Primary language for data science",
                "key_points": ["Python syntax", "NumPy arrays", "Pandas DataFrames", "Data manipulation"],
                "resources": ["Python.org", "NumPy docs", "Pandas documentation"]
            },
            {
                "topic": "Machine Learning Basics",
                "description": "Supervised vs unsupervised learning, model evaluation, and common algorithms.",
                "importance": "Foundation of data science",
                "key_points": ["Supervised learning", "Unsupervised learning", "Evaluation metrics"],
                "resources": ["ML course", "Scikit-learn docs", "ML textbooks"]
            }
        ],
        "intermediate": [
            {
                "topic": "Deep Learning",
                "description": "Neural networks, CNNs, RNNs, and frameworks like TensorFlow/PyTorch.",
                "importance": "Modern approach to complex problems",
                "key_points": ["Neural networks", "CNNs", "RNNs", "Training"],
                "resources": ["Deep Learning", "TensorFlow docs", "PyTorch tutorials"]
            },
            {
                "topic": "Feature Engineering",
                "description": "Creating and selecting features that improve model performance.",
                "importance": "Often more important than the algorithm",
                "key_points": ["Feature creation", "Feature selection", "Scaling", "Encoding"],
                "resources": ["Feature engineering", "ML guide", "Domain knowledge"]
            }
        ],
        "advanced": [
            {
                "topic": "Production ML Systems",
                "description": "Model deployment, monitoring, A/B testing, and MLOps.",
                "importance": "Delivering ML solutions in production",
                "key_points": ["Deployment", "Monitoring", "A/B testing", "MLOps"],
                "resources": ["MLOps guide", "ML systems design", "Production patterns"]
            }
        ]
    }
}
