export const colors = ['#0b84a5', '#f6c85f', '#6f4e7c', '#90c75d', '#ca462f', '#ffa056', '#0c7822', '#1d2da8', '#9b93bf', '#af2db5', '#808080', '#6f4e37'];

export async function fetchComposedReportConfig(data: IFBPayload[]): Promise<ChartConfiguration> {
    return {
		type: 'bar',
		data: prepareGraphData(data),
		options: fetchGraphOptions(data),
	};
}

function fetchGraphOptions(data: IFBPayload[]): ChartOptions {
    return {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        scales: {
            xBar: {
                grid: {
                    display: false
                },
                ticks: {
                    callback: function(val: any) {
                      return this.getLabelForValue(val);
                    },
                    color: 'black',
                    autoSkip: false,
                    font: {
                        size: 15, weight: '500'
                    }
                }
            },
            yBar: {
                position: 'right',
                grid: {
                    drawBorder: false,
                    lineWidth: 0
                },
                ticks: {
                    callback: function(val: any) {
                      return this.getLabelForValue(val);
                    },
                    color: 'black',
                    autoSkip: false,
                    font: {
                        size: 15, weight: '500',
                    }
                }
            },
            yLine: {
                grid: {
                    lineWidth: (ctx) => (ctx.index % 2 === 0 ? 2 : 0),
                    drawBorder: false,
                    borderDash: [3, 3]
                },
                ticks: {
                    callback: function(val: any) {
                        return this.getLabelForValue(val);
                    },
                    major: {
                        enabled: true
                    },
                    color: 'black',
                    autoSkip: false,
                    font: {
                        size: 15, weight: '500'
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'bottom',
                reverse: true,
                labels: {
                  padding: 30,
                  usePointStyle: true,
                  font: {
                      size: 18, weight: '500'
                  },
                  color: '#000000'
                },
            },
            tooltip: {
                bodySpacing: 12,
                bodyFont: {
                    size: 18
                },
                titleAlign: 'center',
                titleColor: '#0097fb',
                callbacks: {
                  label: () => '',
                  beforeBody: (tooltipItem: any) => {
                    const { dataIndex } = tooltipItem[0];
                    const {
                      spend, d1_roas, d7_roas, cpa, cpi, cpm, ppm
                    } = data[dataIndex];
                    return (`
                        SPEND: $${spend || 0}
                        D1 ROAS: ${d1_roas * 100 || 0}%
                        D7 ROAS: ${d7_roas * 100 || 0}%
                        CPA: $${cpa || 0}
                        CPI: $${cpi || 0}
                        CPM: $${cpm || 0}
                        PPM: ${ppm || 0}`);
                  }
                },
            }
        }
    };
}

function prepareGraphData(data: IFBPayload[]): ChartData {

    const barLabel = 'spend';
    const maxSpend = Math.max(...data.map((obj: any) => obj.spend));
    const barData = data.map((obj: any) => obj.spend);
    const lines = ['d1_roas', 'd7_roas'].map((metric, index) => ({ label: metric.toLowerCase(), color: colors[index + 1] }));

    const linesDatasets: ChartDataset[] = lines.map((line, i) => (
        {
            type: 'line',
            label: line.label,
            data: data.map((obj: any) => obj[line.label]),
            backgroundColor: line.color,
            borderColor: line.color,
            borderWidth: 1.5,
            fill: false,
            tension: 0.5,
            cubicInterpolationMode: 'monotone',
            yAxisID: 'yLine',
            order: i,
            pointRadius: 0,
            pointBorderWidth: 3,
            pointHoverBorderWidth: 8
        }
    ));

    return {
        labels: data.map((obj: any) => obj.label),
        datasets: [
          {
            label: barLabel,
            data: barData,
            backgroundColor: barData.map((spend: any) => (spend === maxSpend ? colors[0] : 'rgba(11, 132, 165, 0.5')),
            barThickness: 13,
            borderRadius: Number.MAX_VALUE,
            borderSkipped: false,
            order: 2,
            yAxisID: 'yBar'
          },
          ...linesDatasets
        ],
    };
}