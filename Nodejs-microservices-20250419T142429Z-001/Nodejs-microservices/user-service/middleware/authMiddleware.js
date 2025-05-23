const {expressjwt:jwt} = require('express-jwt');

const authenticateJWT = jwt({
    secret:process.env.JWT_SECRET,
    algorithms:['HS256']
})

module.exports= authenticateJWT;