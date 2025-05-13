# Family Tree App Deployment on Vercel

## Setup

1. Install dependencies:
```
npm install
```

2. Run the development server locally:
```
npm run dev
```

## Serverless Function

- The family tree generation logic from the Python script has been rewritten in Node.js as a serverless function.
- The function is located at `api/generateFamilyTree.js`.
- It accepts POST requests with a JSON body containing `content` (family data text).
- It returns a PNG image of the generated family tree.

## Frontend Integration

- Update your Vue.js frontend to call the serverless function endpoint `/api/generateFamilyTree` with the family data.
- The function will return the generated image which you can display in the UI.

## Notes

- Ensure Graphviz is installed on your deployment environment as the `graphviz` npm package requires the Graphviz binaries.
- On local development, you may need to set the Graphviz path in `api/generateFamilyTree.js` (adjust the `g.setGraphVizPath` line).
- Vercel supports serverless functions in the `api` directory by default.

## Deployment

- Deploy to Vercel using:
```
vercel --prod
