// function checkGraphQLError(userContext, events, done) {
//   const errors = userContext.vars.graphql_errors;
//   if (errors && errors.length > 0) {
//     const msg = errors[0].message || JSON.stringify(errors[0]);
//     console.error("❌ GraphQL Error Detected:", msg);
//     return done(new Error("GraphQL Error: " + msg));
//   }
//   return done();
// }
// module.exports = {
//   checkGraphQLError,
// };

'use strict';

function checkGraphQLResponse(req, res, context, ee, next) {
  try {
    if (res.statusCode !== 200) {
      console.error(`❌ HTTP error: ${res.statusCode}`);
      return next(new Error(`HTTP error: ${res.statusCode}`));
    }

    const body = JSON.parse(res.body);

    if (body.errors && Array.isArray(body.errors) && body.errors.length > 0) {
      const msg = body.errors.map(e => e.message).join(', ') || 'Unknown GraphQL error';
      console.error("❌ GraphQL Error Detected:", msg);
      return next(new Error(`GraphQL error(s): ${msg}`));
    }

    // ✅ Success
    return next(); // lanjut ke langkah berikutnya
  } catch (err) {
    console.error("❌ Invalid JSON or unexpected structure:", err.message);
    return next(new Error("Invalid JSON response"));
  }
}

module.exports = {
  checkGraphQLResponse,
};

