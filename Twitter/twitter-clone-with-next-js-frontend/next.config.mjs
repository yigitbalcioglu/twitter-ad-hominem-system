/** @type {import('next').NextConfig} */
const nextConfig = {
    images:
    {
        remotePatterns: [
            {
                protocol: "http",
                hostname: "localhost",
                port: "1337"
            },
            {
                protocol: "http",
                hostname: "localhost",
                port: "8000"
            },
            {
                protocol: "https",
                hostname: "placehold.co"
            }]
    }
};

export default nextConfig;
