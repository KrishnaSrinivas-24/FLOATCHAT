import FloatChatDashboard from '@/components/FloatChatDashboard';

const Index = () => {
  console.log('Index component rendering...');

  try {
    return <FloatChatDashboard />;
  } catch (error) {
    console.error('Error rendering FloatChatDashboard:', error);
    return (
      <div className="p-8">
        <h1 className="text-4xl font-bold text-red-600">Error Loading Dashboard</h1>
        <p className="text-lg mt-4">Check console for details</p>
      </div>
    );
  }
};

export default Index;
