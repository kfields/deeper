from deeper.setting import decompose

result = decompose({'position': [1,1,1]})
print(result)

result = decompose({ 'Block': {'position': [1,1,1]}})
print(result)

result = decompose({'components': { 'Block': {'position': [1,1,1]}}})
print(result)