const express = require('express');
const { getUsers } = require('../controllers/authController');
const authenticateJWT = require('../middleware/authMiddleware');

const router = express.Router();

router.get('/', authenticateJWT, getUsers);

module.exports = router;
