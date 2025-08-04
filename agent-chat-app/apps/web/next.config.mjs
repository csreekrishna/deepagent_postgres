/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    // Add alias for @ imports
    config.resolve.alias['@'] = new URL('./src', import.meta.url).pathname;
    return config;
  },
};

export default nextConfig;